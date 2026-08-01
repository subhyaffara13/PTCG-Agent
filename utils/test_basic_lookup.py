
def test_basic_lookup():
    assert_equal('{} {}'.format(int(_cd.value('speed of light in vacuum')),
                                _cd.unit('speed of light in vacuum')),
                 '299792458 m s^-1')

