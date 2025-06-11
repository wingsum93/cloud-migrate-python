import subprocess
import pandas as pd
import os

def list_files(remote: str):
    # 透過 rclone lsjson 抓檔案資訊
    result = subprocess.run(["rclone", "lsjson", "-R", remote + ":"], capture_output=True, text=True)
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

    only_in_gdrive = gdrive_set - onedrive_set
    only_in_onedrive = onedrive_set - gdrive_set

    print(f"\n🔍 Files only in Google Drive: {len(only_in_gdrive)}")
    for item in list(only_in_gdrive)[:10]:
        print(" -", item)

    print(f"\n🔍 Files only in OneDrive: {len(only_in_onedrive)}")
    for item in list(only_in_onedrive)[:10]:
        print(" -", item)

    return only_in_gdrive, only_in_onedrive

if __name__ == "__main__":
    print("📥 Fetching Google Drive file list...")
    gdrive_df = list_files("gdrive")

    print("📤 Fetching OneDrive file list...")
    onedrive_df = list_files("onedrive")

    compare_file_lists(gdrive_df, onedrive_df)
