
def test_image_python_io():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3])
    buffer = io.BytesIO()
    fig.savefig(buffer)
    buffer.seek(0)
    plt.imread(buffer)

