
def test_twin_inherit_autoscale_setting():
    fig, ax = plt.subplots()
    ax_x_on = ax.twinx()
    ax.set_autoscalex_on(False)
    ax_x_off = ax.twinx()

    assert ax_x_on.get_autoscalex_on()
    assert not ax_x_off.get_autoscalex_on()

    ax_y_on = ax.twiny()
    ax.set_autoscaley_on(False)
    ax_y_off = ax.twiny()

    assert ax_y_on.get_autoscaley_on()
    assert not ax_y_off.get_autoscaley_on()

