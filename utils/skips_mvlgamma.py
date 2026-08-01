
def skips_mvlgamma(skip_redundant=False):
    skips = (
        # outside domain values are hard error for mvlgamma op.
        DecorateInfo(unittest.skip("Skipped!"), 'TestUnaryUfuncs', 'test_float_domains'),
        DecorateInfo(unittest.expectedFailure, 'TestUnaryUfuncs',
                     'test_reference_numerics_extremal'),
        DecorateInfo(unittest.skip("Skipped!"), 'TestUnaryUfuncs',
                     'test_reference_numerics_large',
                     dtypes=(torch.float16, torch.int8)),
        DecorateInfo(unittest.skip("Skipped!"), 'TestUnaryUfuncs',
                     'test_reference_numerics_small',
                     dtypes=(torch.int8,)),
    )
    if skip_redundant:
        # Redundant tests
        skips = skips + (  # type: ignore[assignment]
            DecorateInfo(unittest.skip("Skipped!"), 'TestFwdGradients'),
            DecorateInfo(unittest.skip("Skipped!"), 'TestBwdGradients'),
            DecorateInfo(unittest.skip("Skipped!"), 'TestJit'),
            DecorateInfo(unittest.skip("Skipped!"), 'TestCommon'),
        )
    return skips

