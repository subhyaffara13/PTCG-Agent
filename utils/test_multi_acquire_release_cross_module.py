
def test_multi_acquire_release_cross_module():
    for bits in range(16 * 8):
        internals_ids = m.test_multi_acquire_release_cross_module(bits)
        assert len(internals_ids) == 2 if bits % 8 else 1

