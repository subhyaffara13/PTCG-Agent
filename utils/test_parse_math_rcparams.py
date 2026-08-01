
def test_parse_math_rcparams():
    # Default is True
    fig, ax = plt.subplots()
    ax.text(0, 0, r"$ \wrong{math} $")
    with pytest.raises(ValueError, match='Unknown symbol'):
        fig.canvas.draw()

    # Setting rcParams to False
    with mpl.rc_context({'text.parse_math': False}):
        fig, ax = plt.subplots()
        ax.text(0, 0, r"$ \wrong{math} $")
        fig.canvas.draw()

