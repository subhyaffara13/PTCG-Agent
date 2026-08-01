
def assert_iinfo_equal(i1, i2):
    # assert two iinfo instances have the same attributes
    for attr in ('bits', 'min', 'max'):
        assert_equal(getattr(i1, attr), getattr(i2, attr),
                     f'iinfo instances {i1} and {i2} differ on {attr}')

