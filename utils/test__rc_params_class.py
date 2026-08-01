
def test_RcParams_class():
    rc = mpl.RcParams({'font.cursive': ['Zapf Chancery', 'cursive'],
                       'font.family': 'sans-serif',
                       'font.weight': 'normal',
                       'font.size': 12})

    expected_repr = """
RcParams({'font.cursive': ['Zapf Chancery', 'cursive'],
          'font.family': ['sans-serif'],
          'font.size': 12.0,
          'font.weight': 'normal'})""".lstrip()

    actual_repr = repr(rc)
    assert actual_repr == expected_repr

    expected_str = """
font.cursive: ['Zapf Chancery', 'cursive']
font.family: ['sans-serif']
font.size: 12.0
font.weight: normal""".lstrip()

    assert str(rc) == expected_str

    # test the find_all functionality
    assert ['font.cursive', 'font.size'] == sorted(rc.find_all('i[vz]'))
    assert ['font.family'] == list(rc.find_all('family'))

