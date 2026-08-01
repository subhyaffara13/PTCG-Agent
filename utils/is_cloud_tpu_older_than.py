
def is_cloud_tpu_older_than(year: int, month: int, day: int, backend):
  if 'TFRT TPU' not in backend.platform_version:
    return False
  # The format of Cloud TPU platform_version is like:
  # PJRT C API
  # TFRT TPU v2
  # Built on Oct 30 2023 03:04:42 (1698660263) cl/577737722
  platform_version = backend.platform_version.split('\n')[-1]
  results = re.findall(r'\(.*?\)', platform_version)
  if len(results) != 1:
    return True
  date = datetime.date(year, month, day)
  build_date = date.fromtimestamp(int(results[0][1:-1]))
  # Filter out ridiculously old dates that some test builds get.
  return build_date < date and build_date.year > 2010

