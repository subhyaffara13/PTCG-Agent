
def test_no_duplicate_definition():

    fig = Figure()
    axs = fig.subplots(4, 4, subplot_kw=dict(projection="polar"))
    for ax in axs.flat:
        ax.set(xticks=[], yticks=[])
        ax.plot([1, 2])
    fig.suptitle("hello, world")

    buf = io.StringIO()
    fig.savefig(buf, format='eps')
    buf.seek(0)

    wds = [ln.partition(' ')[0] for
           ln in buf.readlines()
           if ln.startswith('/')]

    assert max(Counter(wds).values()) == 1

