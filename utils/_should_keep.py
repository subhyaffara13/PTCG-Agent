
def _should_keep(entry, keep_files, suffixes):
    return entry.name in keep_files or entry.suffix in suffixes

