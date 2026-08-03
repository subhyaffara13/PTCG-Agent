import os

def test_savefig(kind, data, index):
    fig, ax = plt.subplots()
    data.index = index
    kwargs = {}
    if kind in ["hexbin", "scatter", "pie"]:
        if isinstance(data, Series):
            pytest.skip(f"{kind} not supported with Series")
        kwargs = {"x": 0, "y": 1}
    data.plot(kind=kind, ax=ax, **kwargs)
    fig.savefig(os.devnull)


def test_savefig():
    fig = plt.figure()
    msg = r"savefig\(\) takes 2 positional arguments but 3 were given"
    with pytest.raises(TypeError, match=msg):
        fig.savefig("fname1.png", "fname2.png")

