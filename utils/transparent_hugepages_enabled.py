
def transparent_hugepages_enabled() -> bool:
  # See https://docs.kernel.org/admin-guide/mm/transhuge.html for more
  # information about transparent huge pages.
  path = pathlib.Path('/sys/kernel/mm/transparent_hugepage/enabled')
  return path.exists() and path.read_text().strip() == '[always] madvise never'

