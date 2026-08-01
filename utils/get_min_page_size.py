
def get_min_page_size(max_model_len, min_page_size=16):
  """Recommended min page size for high-performance kernel."""
  return max(next_power_of_2(max_model_len) // MAX_PAGES_PER_SEQ, min_page_size)

