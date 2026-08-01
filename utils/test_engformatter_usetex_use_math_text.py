
def test_engformatter_usetex_useMathText():
    fig, ax = plt.subplots()
    ax.plot([0, 500, 1000], [0, 500, 1000])
    ax.set_xticks([0, 500, 1000])
    for formatter in (mticker.EngFormatter(usetex=True),
                      mticker.EngFormatter(useMathText=True)):
        ax.xaxis.set_major_formatter(formatter)
        fig.canvas.draw()
        x_tick_label_text = [labl.get_text() for labl in ax.get_xticklabels()]
        # Checking if the dollar `$` signs have been inserted around numbers
        # in tick labels.
        assert x_tick_label_text == ['$0$', '$500$', '$1$ k']

