
def get_byte_limiter(
    concurrent_bytes: int, sleep_time: float
) -> TestLimitInFlightBytes:
  return TestLimitInFlightBytes(concurrent_bytes, sleep_time)


def get_byte_limiter(concurrent_bytes: Optional[int] = None) -> ByteLimiter:
  if concurrent_bytes is None:
    return UnlimitedInFlightBytes()
  if concurrent_bytes <= 0:
    raise ValueError(
        f'Must provide positive `concurrent_bytes`. Found: {concurrent_bytes}'
    )
  return LimitInFlightBytes(concurrent_bytes)

