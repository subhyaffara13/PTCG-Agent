
def test_patch_edgegapcolor_visual():
    """Visual test for patch edgegapcolor (striped edges)."""
    fig, ax = plt.subplots()

    # Rectangle with edgegapcolor
    rect = Rectangle((0.1, 0.1), 0.3, 0.3, fill=False,
                      edgecolor='blue', edgegapcolor='orange',
                      linestyle='--', linewidth=3)
    ax.add_patch(rect)

    # Ellipse with edgegapcolor
    ellipse = Ellipse((0.7, 0.3), 0.3, 0.2, fill=False,
                       edgecolor='red', edgegapcolor='yellow',
                       linestyle=':', linewidth=3)
    ax.add_patch(ellipse)

    # Polygon with edgegapcolor
    polygon = Polygon([[0.1, 0.6], [0.3, 0.9], [0.4, 0.6]], fill=False,
                       edgecolor='green', edgegapcolor='purple',
                       linestyle='-.', linewidth=3)
    ax.add_patch(polygon)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')

