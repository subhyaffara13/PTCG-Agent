
def is_cloud_tpu_at_least(year: int, month: int, day: int) -> bool:
  date = datetime.date(year, month, day)
  if not is_cloud_tpu():
    return True
  # The format of Cloud TPU platform_version is like:
  # PJRT C API
  # TFRT TPU v2
  # Built on Oct 30 2023 03:04:42 (1698660263) cl/577737722
  platform_version = xla_bridge.get_backend().platform_version.split('\n')[-1]
  results = re.findall(r'\(.*?\)', platform_version)
  if len(results) != 1:
    return True
  build_date = date.fromtimestamp(int(results[0][1:-1]))
  return build_date >= date

