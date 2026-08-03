from pathlib import Path


def test_closed_path_clipping(fig_test, fig_ref):
    vertices = []
    for roll in range(8):
        offset = 0.1 * roll + 0.1

        # A U-like pattern.
        pattern = [
            [-0.5, 1.5], [-0.5, -0.5], [1.5, -0.5], [1.5, 1.5],  # Outer square
            # With a notch in the top.
            [1 - offset / 2, 1.5], [1 - offset / 2, offset],
            [offset / 2, offset], [offset / 2, 1.5],
        ]

        # Place the initial/final point anywhere in/out of the clipping area.
        pattern = np.roll(pattern, roll, axis=0)
        pattern = np.concatenate((pattern, pattern[:1, :]))

        vertices.append(pattern)

    # Multiple subpaths are used here to ensure they aren't broken by closed
    # loop clipping.
    codes = np.full(len(vertices[0]), Path.LINETO)
    codes[0] = Path.MOVETO
    codes[-1] = Path.CLOSEPOLY
    codes = np.tile(codes, len(vertices))
    vertices = np.concatenate(vertices)

    fig_test.set_size_inches((5, 5))
    path = Path(vertices, codes)
    fig_test.add_artist(patches.PathPatch(path, facecolor='none'))

    # For reference, we draw the same thing, but unclosed by using a line to
    # the last point only.
    fig_ref.set_size_inches((5, 5))
    codes = codes.copy()
    codes[codes == Path.CLOSEPOLY] = Path.LINETO
    path = Path(vertices, codes)
    fig_ref.add_artist(patches.PathPatch(path, facecolor='none'))

