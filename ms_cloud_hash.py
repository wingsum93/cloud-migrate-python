import requests
import json

access_token = "1d5507c5-39b2-4891-8839-1d30f74a780b"  # ⚠️ 需要 OAuth2 login 先取得

headers = {
    "Authorization": f"Bearer {access_token}"
}
onedrive_file_path = "/path/to/your/file.txt"

# ✅ 呼叫 Graph API，取得檔案的 hash
url = f"https://graph.microsoft.com/v1.0/me/drive/root:{onedrive_file_path}?"
params = {"select": "name,file"}

response = requests.get(url, headers=headers, params=params)

# ✅ 顯示回傳結果
if response.status_code == 200:
    data = response.json()
    hash_value = data.get("file", {}).get("hashes", {}).get("quickXorHash")
    if hash_value:
        print("✅ QuickXorHash:", hash_value)
    else:
        print("⚠️ This file has no QuickXorHash info.")
else:
    print("❌ Failed to get file info:", response.status_code)
    print(response.text)