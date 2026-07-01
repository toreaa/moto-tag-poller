from KeyBackup.shared_key_retrieval import get_shared_key
k = get_shared_key()
print(f"SHARED_KEY_OK len={len(k)}", flush=True)
