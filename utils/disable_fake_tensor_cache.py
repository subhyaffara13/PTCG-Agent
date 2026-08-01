
def disable_fake_tensor_cache(fake_mode: FakeTensorMode) -> Generator[None, None, None]:
    old_value: bool = fake_mode.cache_enabled
    try:
        fake_mode.cache_enabled = False
        yield
    finally:
        fake_mode.cache_enabled = old_value

