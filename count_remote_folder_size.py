import subprocess
import pandas as pd
import argparse
import os

def list_files(remote: str, path: str):
    full_remote = f"{remote}:{path}".replace("\\", "/")
    result = subprocess.run(["rclone", "lsjson", "-R", full_remote], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"❌ Error accessing {full_remote}")
        print(result.stderr)
        return pd.DataFrame()
    try:
        df = pd.read_json(result.stdout)
        if not path.endswith("/"):
            path += "/"
        df["Path"] = df["Path"].apply(lambda p: p.replace("\\", "/"))  # normalize slashes
        return df
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        return pd.DataFrame()

def compute_subfolder_stats(df: pd.DataFrame):
    if df.empty:
        print("⚠️ No files found.")
        return

    df = df[df["IsDir"] == False]  # 只處理檔案

    # 分析每個檔案屬於邊個子資料夾
    def get_first_folder(path):
        parts = path.split("/")
        return parts[0] if len(parts) > 1 else "<ROOT>"

    df["Folder"] = df["Path"].apply(get_first_folder)

    grouped = df.groupby("Folder").agg(
        FileCount=("Size", "count"),
        TotalSize=("Size", "sum")
    ).sort_values(by="TotalSize", ascending=False)

    print("\n📊 Subfolder Statistics:")
    for folder, row in grouped.iterrows():
        size_mb = row["TotalSize"] / (1024 * 1024)
        print(f" - {folder:<30} | {row['FileCount']:>4} files | {size_mb:.2f} MB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count total size and file count of subfolders in a remote path")
    parser.add_argument("remote", type=str, help="Remote name (e.g., gdrive, onedrive)")
    parser.add_argument("path", type=str, help="Remote folder path (e.g., /myfolder)")
    args = parser.parse_args()

    df = list_files(args.remote, args.path)
    compute_subfolder_stats(df)
