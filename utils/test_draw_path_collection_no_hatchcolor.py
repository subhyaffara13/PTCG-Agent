
def test_draw_path_collection_no_hatchcolor(backend):
    from matplotlib.collections import PathCollection
    path = mpath.Path.unit_rectangle()

    plt.switch_backend(backend)
    fig, ax = plt.subplots()
    renderer = fig._get_renderer()

    col = PathCollection([path], hatch='//')
    ax.add_collection(col)

    gc = renderer.new_gc()
    transform = mtransforms.IdentityTransform()
    paths = col.get_paths()
    transforms = col.get_transforms()
    offsets = col.get_offsets()
    offset_trf = col.get_offset_transform()
    facecolors = col.get_facecolor()
    edgecolors = col.get_edgecolor()
    linewidths = col.get_linewidth()
    linestyles = col.get_linestyle()
    antialiaseds = col.get_antialiased()
    urls = col.get_urls()
    offset_position = "screen"

    renderer.draw_path_collection(
        gc, transform, paths, transforms, offsets, offset_trf,
        facecolors, edgecolors, linewidths, linestyles,
        antialiaseds, urls, offset_position
    )

