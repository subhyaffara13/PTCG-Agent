
def test_animation_with_transparency():
    """Test animation exhaustion with transparency using PillowWriter directly"""
    fig, ax = plt.subplots()
    rect = plt.Rectangle((0, 0), 1, 1, color='red', alpha=0.5)
    ax.add_patch(rect)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    writer = PillowWriter(fps=30)
    writer.setup(fig, 'unused.gif', dpi=100)
    writer.grab_frame(transparent=True)
    frame = writer._frames[-1]
    # Check that the alpha channel is not 255, so frame has transparency
    assert frame.getextrema()[3][0] < 255
    plt.close(fig)

