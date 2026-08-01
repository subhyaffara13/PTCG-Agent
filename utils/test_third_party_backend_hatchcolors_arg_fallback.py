
def test_third_party_backend_hatchcolors_arg_fallback(monkeypatch):
    fig, ax = plt.subplots()
    canvas = fig.canvas
    renderer = canvas.get_renderer()

    # monkeypatch the `draw_path_collection` method to simulate a third-party backend
    # that does not support the `hatchcolors` argument.
    def mock_draw_path_collection(self, gc, master_transform, paths, all_transforms,
                                  offsets, offset_trans, facecolors, edgecolors,
                                  linewidths, linestyles, antialiaseds, urls,
                                  offset_position):
        pass

    monkeypatch.setattr(renderer, 'draw_path_collection', mock_draw_path_collection)

    # Create a PathCollection with hatch colors
    from matplotlib.collections import PathCollection
    path = mpath.Path.unit_rectangle()
    coll = PathCollection([path], hatch='//', hatchcolor='red')

    ax.add_collection(coll)

    plt.draw()

