
def test_parse_math():
    fig, ax = plt.subplots()
    ax.text(0, 0, r"$ \wrong{math} $", parse_math=False)
    fig.canvas.draw()

    ax.text(0, 0, r"$ \wrong{math} $", parse_math=True)
    with pytest.raises(ValueError, match='Unknown symbol'):
        fig.canvas.draw()

