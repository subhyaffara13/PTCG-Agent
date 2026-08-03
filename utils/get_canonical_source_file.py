import re

def get_canonical_source_file(file_name: str, caches: TracebackCaches) -> str:
  canonical_file_name = caches.canonical_name_cache.get(file_name, None)
  if canonical_file_name is not None:
    return canonical_file_name

  pattern = config.hlo_source_file_canonicalization_regex.value
  if pattern:
    file_name = re.sub(pattern, '', file_name)
  caches.canonical_name_cache[file_name] = file_name
  return file_name

