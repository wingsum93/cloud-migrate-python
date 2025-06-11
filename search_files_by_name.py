import subprocess
import pandas as pd
import argparse
from datetime import datetime

def list_files(remote: str):
    result = subprocess.run(["rclone", "lsjson", "-R", f"{remote}:"], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"❌ Error accessing remote '{remote}'")
        print(result.stderr)
        return pd.DataFrame()
    try:
        return pd.read_json(result.stdout)
    except Exception as e:
        print("❌ Failed to parse JSON from rclone output:", e)
        return pd.DataFrame()

def search_files(df: pd.DataFrame, keyword: str):
    if df.empty:
        print("⚠️ No files found.")
        return

    df = df[df["IsDir"] == False].copy()  # 過濾資料夾
    df["ModTime"] = pd.to_datetime(df["ModTime"], utc=True)

    # 做大小寫不敏感搜尋：搜尋 keyword 喺 Path or Name 裡面出現
    mask = df["Path"].str.contains(keyword, case=False) | df["Name"].str.contains(keyword, case=False)
    result_df = df[mask].copy()

    if result_df.empty:
        print(f"🔍 No results found for keyword: {keyword}")
        return

    print(f"\n🔎 Found {len(result_df)} matching files for keyword: '{keyword}'\n")
    for _, row in result_df.sort_values(by="Size", ascending=False).iterrows():
        size_mb = row["Size"] / (1024 * 1024)
        mod_time = row["ModTime"].strftime("%Y-%m-%d %H:%M:%S")
        print(f" - {row['Path']} | {size_mb:.2f} MB | Modified: {mod_time}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for files in rclone remote by name or folder path.")
    parser.add_argument("remote", type=str, help="Name of rclone remote (e.g., onedrive, gdrive)")
    parser.add_argument("keyword", type=str, help="Keyword to search in file name or folder path")
    args = parser.parse_args()

    df = list_files(args.remote)
    search_files(df, args.keyword)
