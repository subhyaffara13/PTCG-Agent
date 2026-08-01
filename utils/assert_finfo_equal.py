
def assert_finfo_equal(f1, f2):
    # assert two finfo instances have the same attributes
    for attr in ('bits', 'eps', 'epsneg', 'iexp', 'machep',
                 'max', 'maxexp', 'min', 'minexp', 'negep', 'nexp',
                 'nmant', 'precision', 'resolution', 'tiny',
                 'smallest_normal', 'smallest_subnormal'):
        assert_equal(getattr(f1, attr), getattr(f2, attr),
                     f'finfo instances {f1} and {f2} differ on {attr}')

