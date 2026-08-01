
def test_check_shape(target: tuple[int | None, ...],
                     shape_repr: str,
                     test_shape: tuple[int, ...]) -> None:
    error_pattern = "^" + re.escape(
        f"'aardvark' must be {len(target)}D with shape {shape_repr}, but your input "
        f"has shape {test_shape}")
    data = np.zeros(test_shape)
    with pytest.raises(ValueError, match=error_pattern):
        _api.check_shape(target, aardvark=data)

