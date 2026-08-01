
def test_basic_table_parse():
    c_s = 'speed of light in vacuum'
    assert_equal(value(c_s), c)
    assert_equal(value(c_s), speed_of_light)

