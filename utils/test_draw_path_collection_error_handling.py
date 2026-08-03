from pathlib import Path


def test_draw_path_collection_error_handling():
    fig, ax = plt.subplots()
    ax.scatter([1], [1]).set_paths(Path([(0, 1), (2, 3)]))
    with pytest.raises(TypeError):
        fig.canvas.draw()

