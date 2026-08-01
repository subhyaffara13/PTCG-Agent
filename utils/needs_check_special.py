
def needs_check_special() -> bool:
  return config.debug_infs.value or config.debug_nans.value

