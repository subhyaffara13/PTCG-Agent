
def test_vector_derivative_printing():
    # First order
    v = omega.diff() * N.x
    assert unicode_vpretty(v) == 'ω̇ n_x'
    assert ascii_vpretty(v) == "omega'(t) n_x"

    # Second order
    v = omega.diff().diff() * N.x

    assert vlatex(v) == r'\ddot{\omega}\mathbf{\hat{n}_x}'
    assert unicode_vpretty(v) == 'ω̈ n_x'
    assert ascii_vpretty(v) == "omega''(t) n_x"

    # Third order
    v = omega.diff().diff().diff() * N.x

    assert vlatex(v) == r'\dddot{\omega}\mathbf{\hat{n}_x}'
    assert unicode_vpretty(v) == 'ω⃛ n_x'
    assert ascii_vpretty(v) == "omega'''(t) n_x"

    # Fourth order
    v = omega.diff().diff().diff().diff() * N.x

    assert vlatex(v) == r'\ddddot{\omega}\mathbf{\hat{n}_x}'
    assert unicode_vpretty(v) == 'ω⃜ n_x'
    assert ascii_vpretty(v) == "omega''''(t) n_x"

    # Fifth order
    v = omega.diff().diff().diff().diff().diff() * N.x

    assert vlatex(v) == r'\frac{d^{5}}{d t^{5}} \omega\mathbf{\hat{n}_x}'
    expected = '''\
 5            \n\
d             \n\
---(omega) n_x\n\
  5           \n\
dt            \
'''
    uexpected = '''\
 5        \n\
d         \n\
───(ω) n_x\n\
  5       \n\
dt        \
'''
    assert unicode_vpretty(v) == uexpected
    assert ascii_vpretty(v) == expected

