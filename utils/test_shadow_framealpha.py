
def test_shadow_framealpha():
    # Test if framealpha is activated when shadow is True
    # and framealpha is not explicitly passed'''
    fig, ax = plt.subplots()
    ax.plot(range(100), label="test")
    leg = ax.legend(shadow=True, facecolor='w')
    assert leg.get_frame().get_alpha() == 1

