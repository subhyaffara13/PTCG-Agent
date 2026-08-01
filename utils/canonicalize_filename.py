
def canonicalize_filename(file_name: str):
  pattern = config.hlo_source_file_canonicalization_regex.value
  if pattern:
    file_name = re.sub(pattern, '', file_name)
  return file_name

