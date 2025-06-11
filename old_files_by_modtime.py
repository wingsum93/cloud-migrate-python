import subprocess
import pandas as pd
import argparse
from datetime import datetime
from datetime import timezone

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

def show_oldest_files(df: pd.DataFrame, top_n: int = 20):
    if df.empty:
        print("⚠️ No files found.")
        return

    df = df[df["IsDir"] == False].copy()  # 過濾資料夾
    df["ModTime"] = pd.to_datetime(df["ModTime"])
    df = df.sort_values(by="ModTime", ascending=True).head(top_n)

    print(f"\n📜 Top {top_n} oldest files by last modified date:")
    for _, row in df.iterrows():
        age_days = (datetime.now(timezone.utc) - row["ModTime"]).days
        size_mb = row["Size"] / (1024 * 1024)
        print(f" - {row['Path']} ({size_mb:.2f} MB, modified {row['ModTime'].date()} - {age_days} days ago)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List oldest files in remote based on last modified date")
    parser.add_argument("remote", type=str, help="Name of rclone remote (e.g., onedrive, gdrive)")
    parser.add_argument("--top", type=int, default=20, help="Number of old files to show (default: 20)")
    args = parser.parse_args()

    df = list_files(args.remote)
    show_oldest_files(df, top_n=args.top)
