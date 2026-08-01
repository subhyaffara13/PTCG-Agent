
def test_gh_19423(dt, xp):
    rng = np.random.default_rng(123)
    max_val = 8
    image = rng.integers(low=0, high=max_val, size=(10, 12)).astype(dtype=dt)
    val_idx = ndimage.value_indices(image)
    assert len(val_idx.keys()) == max_val

