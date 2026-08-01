
def sanitize_test_name(s: str) -> str:
  return kSanitizeNameRE.sub("_", s)

