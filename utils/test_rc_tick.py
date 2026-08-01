
def test_rc_tick():
    d = {'xtick.bottom': False, 'xtick.top': True,
         'ytick.left': True, 'ytick.right': False}
    with plt.rc_context(rc=d):
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        xax = ax1.xaxis
        yax = ax1.yaxis
        # tick1On bottom/left
        assert not xax._major_tick_kw['tick1On']
        assert xax._major_tick_kw['tick2On']
        assert not xax._minor_tick_kw['tick1On']
        assert xax._minor_tick_kw['tick2On']

        assert yax._major_tick_kw['tick1On']
        assert not yax._major_tick_kw['tick2On']
        assert yax._minor_tick_kw['tick1On']
        assert not yax._minor_tick_kw['tick2On']

