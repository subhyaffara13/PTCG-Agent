
def test_tex_restart_after_error():
    fig = plt.figure()
    fig.suptitle(r"\oops")
    with pytest.raises(ValueError):
        fig.savefig(BytesIO(), format="pgf")

    fig = plt.figure()  # start from scratch
    fig.suptitle(r"this is ok")
    fig.savefig(BytesIO(), format="pgf")

