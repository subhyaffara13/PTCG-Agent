def _should_keep(entry, keep_files, suffixes):
    return entry.name in keep_files or entry.suffix in suffixes

def _prune_entry(entry, cutoff, keep_set, suffixes, prunable_prefixes):
    if entry.is_dir() and any(entry.name.startswith(p) for p in prunable_prefixes):
        import shutil
        try:
            if entry.stat().st_mtime < cutoff: shutil.rmtree(entry); return True
        except Exception: pass
        return False
    if not entry.is_file(): return False
    if _should_keep(entry, keep_set, suffixes): return False
    if entry.name.startswith(prunable_prefixes) and entry.suffix == ".json":
        try:
            if entry.stat().st_mtime < cutoff: entry.unlink(); return True
        except Exception: pass
    return False
