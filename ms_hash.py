import base64


def quickxorhash(file_path):
    length = 0
    buffer = bytearray(20)
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            for i in range(len(chunk)):
                buffer[i % 20] ^= chunk[i]
            length += len(chunk)

    buffer[-1] ^= length & 0xFF
    buffer[-2] ^= (length >> 8) & 0xFF
    buffer[-3] ^= (length >> 16) & 0xFF
    return buffer.hex()

def quickxorhash_base64(file_path):
    raw = bytes.fromhex(quickxorhash(file_path))
    return base64.b64encode(raw).decode("utf-8")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Calculate QuickXorHash for a file.")
    parser.add_argument("file_path", type=str, help="Path to the file to hash")
    args = parser.parse_args()

    hash_value = quickxorhash_base64(args.file_path)
    print(f"QuickXorHash (Base64): {hash_value}")