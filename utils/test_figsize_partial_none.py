
def test_figsize_partial_none():
    default_w, default_h = mpl.rcParams["figure.figsize"]

    fig = plt.figure(figsize=(None, 4))
    w, h = fig.get_size_inches()
    assert (w, h) == (default_w, 4)

    fig = plt.figure(figsize=(6, None))
    w, h = fig.get_size_inches()
    assert (w, h) == (6, default_h)

