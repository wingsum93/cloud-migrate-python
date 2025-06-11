import subprocess
import pandas as pd
import os

def list_files(remote: str):
    # 透過 rclone lsjson 抓檔案資訊
    result = subprocess.run(["rclone", "lsjson", "-R", remote + ":"], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"Error listing files from {remote}")
        print(result.stderr)
        return []
    return pd.read_json(result.stdout)

def compare_file_lists(gdrive_df, onedrive_df):
    # 用 path + size 作為唯一識別
    gdrive_df["id"] = gdrive_df["Path"] + "::" + gdrive_df["Size"].astype(str)
    onedrive_df["id"] = onedrive_df["Path"] + "::" + onedrive_df["Size"].astype(str)

    gdrive_set = set(gdrive_df["id"])
    onedrive_set = set(onedrive_df["id"])

    only_in_gdrive_ids = gdrive_set - onedrive_set
    only_in_onedrive_ids = onedrive_set - gdrive_set
    in_both_ids = gdrive_set & onedrive_set  # 新增：交集（兩邊都有）

    # 篩選出原始資料
    only_in_gdrive = gdrive_df[gdrive_df["id"].isin(only_in_gdrive_ids)].sort_values(by="Size", ascending=False)
    only_in_onedrive = onedrive_df[onedrive_df["id"].isin(only_in_onedrive_ids)].sort_values(by="Size", ascending=False)
    in_both = gdrive_df[gdrive_df["id"].isin(in_both_ids)].sort_values(by="Size", ascending=False)

    def format_entry(path,size_bytes):   
        size_mb = int(size_bytes) / (1024 * 1024)
        return f"{path} ({size_mb:.2f} MB)"
    
    # 輸出前 10 個結果
    print(f"\n📂 Files only in Google Drive: {len(only_in_gdrive)}")
    for _, row in only_in_gdrive.head(10).iterrows():
        print(" -", format_entry(row["Path"], row["Size"]))

    print(f"\n📂 Files only in OneDrive: {len(only_in_onedrive)}")
    for _, row in only_in_onedrive.head(10).iterrows():
        print(" -", format_entry(row["Path"], row["Size"]))

    print(f"\n✅ Files present in both platforms: {len(in_both_ids)}")
    for _, row in in_both.head(10).iterrows():
        print(" -", format_entry(row["Path"], row["Size"]))
    return only_in_gdrive, only_in_onedrive, in_both

if __name__ == "__main__":
    print("📥 Fetching Google Drive file list...")
    gdrive_df = list_files("gdrive")

    print("📤 Fetching OneDrive file list...")
    onedrive_df = list_files("onedrive")

    only_in_gdrive, only_in_onedrive, in_both_ids = compare_file_lists(gdrive_df, onedrive_df)
