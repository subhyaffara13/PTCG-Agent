
def skip_nan_unexpected_exception():
    try:
        # should not raise an exception
        with np.errstate(all='raise'):
            x = np.asarray([1, 2, np.nan])
            np.mean(x)
    except Exception as e:
        pytest.skip(f"nan raises unexpected {e.__class__.__name__} in numpy")

