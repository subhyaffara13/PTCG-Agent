
def test_translate_tick_params_reverse():
    fig, ax = plt.subplots()
    kw = {'label1On': 'a', 'label2On': 'b', 'tick1On': 'c', 'tick2On': 'd'}
    assert (ax.xaxis._translate_tick_params(kw, reverse=True) ==
            {'labelbottom': 'a', 'labeltop': 'b', 'bottom': 'c', 'top': 'd'})
    assert (ax.yaxis._translate_tick_params(kw, reverse=True) ==
            {'labelleft': 'a', 'labelright': 'b', 'left': 'c', 'right': 'd'})

