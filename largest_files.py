import subprocess
import pandas as pd
import argparse

def list_files(remote: str):
    result = subprocess.run(["rclone", "lsjson", "-R", remote + ":"], capture_output=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"❌ Error accessing {remote}")
        print(result.stderr)
        return pd.DataFrame()
    try:
        return pd.read_json(result.stdout)
    except Exception as e:
        print("❌ Failed to parse JSON from rclone output:", e)
        return pd.DataFrame()

def show_largest_files(df: pd.DataFrame, top_n: int = 20):
    if df.empty:
        print("⚠️ No files found.")
        return

    df = df[df["IsDir"] == False]  # 過濾資料夾
    df = df.sort_values(by="Size", ascending=False).head(top_n)

    def format_entry(path, size_bytes):
        size_mb = size_bytes / (1024 * 1024)
        return f"{path} ({size_mb:.2f} MB)"

    print(f"\n📦 Top {top_n} largest files in OneDrive:")
    for _, row in df.iterrows():
        print(" -", format_entry(row["Path"], row["Size"]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show largest files in a rclone remote")
    parser.add_argument("remote", type=str, help="Name of rclone remote (e.g., onedrive, gdrive)")
    parser.add_argument("--top", type=int, default=20, help="Number of top largest files to show (default: 20)")
    args = parser.parse_args()

    df = list_files(args.remote)
    show_largest_files(df, top_n=args.top)
