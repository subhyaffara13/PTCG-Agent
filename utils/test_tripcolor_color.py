
def test_tripcolor_color():
    x = [-1, 0, 1, 0]
    y = [0, -1, 0, 1]
    fig, ax = plt.subplots()
    with pytest.raises(TypeError, match=r"tripcolor\(\) missing 1 required "):
        ax.tripcolor(x, y)
    with pytest.raises(ValueError, match="The length of c must match either"):
        ax.tripcolor(x, y, [1, 2, 3])
    with pytest.raises(ValueError,
                       match="length of facecolors must match .* triangles"):
        ax.tripcolor(x, y, facecolors=[1, 2, 3, 4])
    with pytest.raises(ValueError,
                       match="'gouraud' .* at the points.* not at the faces"):
        ax.tripcolor(x, y, facecolors=[1, 2], shading='gouraud')
    with pytest.raises(ValueError,
                       match="'gouraud' .* at the points.* not at the faces"):
        ax.tripcolor(x, y, [1, 2], shading='gouraud')  # faces
    with pytest.raises(TypeError,
                       match="positional.*'c'.*keyword-only.*'facecolors'"):
        ax.tripcolor(x, y, C=[1, 2, 3, 4])
    with pytest.raises(TypeError, match="Unexpected positional parameter"):
        ax.tripcolor(x, y, [1, 2], 'unused_positional')

    # smoke test for valid color specifications (via C or facecolors)
    ax.tripcolor(x, y, [1, 2, 3, 4])  # edges
    ax.tripcolor(x, y, [1, 2, 3, 4], shading='gouraud')  # edges
    ax.tripcolor(x, y, [1, 2])  # faces
    ax.tripcolor(x, y, facecolors=[1, 2])  # faces

