
def read_files_in_batches(files, max_chars=30000):
    batches = []
    current_batch = ""
    for f in files:
        try:
            content = f.read_text(encoding="utf-8")
            chunk = f"\n\n--- FILE: {f} ---\n{content}"
            if len(current_batch) + len(chunk) > max_chars:
                batches.append(current_batch)
                current_batch = chunk
            else:
                current_batch += chunk
        except Exception:
            pass
    if current_batch:
        batches.append(current_batch)
    return batches

