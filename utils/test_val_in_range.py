
def test_val_in_range():

    test_cases = [
        # LinearScale: Always True (even for Inf/NaN)
        ('linear', 10.0, True),
        ('linear', -10.0, True),
        ('linear', 0.0, True),
        ('linear', np.inf, False),
        ('linear', np.nan, False),

        # LogScale: Only positive values (> 0)
        ('log', 1.0, True),
        ('log', 1e-300, True),
        ('log', 0.0, False),
        ('log', -1.0, False),
        ('log', np.inf, False),
        ('log', np.nan, False),

        # LogitScale: Strictly between 0 and 1
        ('logit', 0.5, True),
        ('logit', 0.0, False),
        ('logit', 1.0, False),
        ('logit', -0.1, False),
        ('logit', 1.1, False),
        ('logit', np.inf, False),
        ('logit', np.nan, False),

        # SymmetricalLogScale: Valid for all real numbers
        # Uses ScaleBase fallback. NaN returns False since NaN != NaN
        ('symlog', 10.0, True),
        ('symlog', -10.0, True),
        ('symlog', 0.0, True),
        ('symlog', np.inf, False),
        ('symlog', np.nan, False),
    ]

    for name, val, expected in test_cases:
        scale_cls = mscale._scale_mapping[name]
        s = scale_cls(axis=None)

        result = s.val_in_range(val)
        assert result is expected, (
            f"Failed {name}.val_in_range({val})."
            f"Expected {expected}, got {result}"
        )

