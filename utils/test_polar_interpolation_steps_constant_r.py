
def test_polar_interpolation_steps_constant_r(fig_test, fig_ref):
    # Check that an extra half-turn doesn't make any difference -- modulo
    # antialiasing, which we disable here.
    p1 = (fig_test.add_subplot(121, projection="polar")
          .bar([0], [1], 3*np.pi, edgecolor="none", antialiased=False))
    p2 = (fig_test.add_subplot(122, projection="polar")
          .bar([0], [1], -3*np.pi, edgecolor="none", antialiased=False))
    p3 = (fig_ref.add_subplot(121, projection="polar")
          .bar([0], [1], 2*np.pi, edgecolor="none", antialiased=False))
    p4 = (fig_ref.add_subplot(122, projection="polar")
          .bar([0], [1], -2*np.pi, edgecolor="none", antialiased=False))

