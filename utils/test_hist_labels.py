
def test_hist_labels():
    # test singleton labels OK
    fig, ax = plt.subplots()
    _, _, bars = ax.hist([0, 1], label=0)
    assert bars[0].get_label() == '0'
    _, _, bars = ax.hist([0, 1], label=[0])
    assert bars[0].get_label() == '0'
    _, _, bars = ax.hist([0, 1], label=None)
    assert bars[0].get_label() == '_nolegend_'
    _, _, bars = ax.hist([0, 1], label='0')
    assert bars[0].get_label() == '0'
    _, _, bars = ax.hist([0, 1], label='00')
    assert bars[0].get_label() == '00'

