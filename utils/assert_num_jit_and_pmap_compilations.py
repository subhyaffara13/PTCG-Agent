
def assert_num_jit_and_pmap_compilations(times):
  with count_jit_and_pmap_lowerings() as count:
    yield
  if count() != times:
    raise AssertionError(f"Expected exactly {times} XLA compilations, "
                         f"but executed {count()}")

