
def _bytes_to_date(s):
    return date(*time.strptime(s, "%Y-%m-%d")[:3])

