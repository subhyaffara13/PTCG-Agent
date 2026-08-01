
def _version_from_todays_date(base_version: str) -> str:
  datestring = datetime.date.today().strftime("%Y%m%d")
  return f"{base_version}.dev{datestring}"


def _version_from_todays_date(base_version: str) -> str:
  datestring = datetime.date.today().strftime("%Y%m%d")
  return f"{base_version}.dev{datestring}"

