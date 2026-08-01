
def test_plot_format_errors(fmt, match, data):
    fig, ax = plt.subplots()
    if data is not None:
        match = match.replace("not", "neither a data key nor")
    with pytest.raises(ValueError, match=r"\A" + match + r"\Z"):
        ax.plot("string", fmt, data=data)

