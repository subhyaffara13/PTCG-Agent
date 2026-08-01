
def _test_number_of_draws_script():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    # animated=True tells matplotlib to only draw the artist when we
    # explicitly request it
    ln, = ax.plot([0, 1], [1, 2], animated=True)

    # make sure the window is raised, but the script keeps going
    plt.show(block=False)
    plt.pause(0.3)
    # Connect to draw_event to count the occurrences
    fig.canvas.mpl_connect('draw_event', print)

    # get copy of entire figure (everything inside fig.bbox)
    # sans animated artist
    bg = fig.canvas.copy_from_bbox(fig.bbox)
    # draw the animated artist, this uses a cached renderer
    ax.draw_artist(ln)
    # show the result to the screen
    fig.canvas.blit(fig.bbox)

    for j in range(10):
        # reset the background back in the canvas state, screen unchanged
        fig.canvas.restore_region(bg)
        # Create a **new** artist here, this is poor usage of blitting
        # but good for testing to make sure that this doesn't create
        # excessive draws
        ln, = ax.plot([0, 1], [1, 2])
        # render the artist, updating the canvas state, but not the screen
        ax.draw_artist(ln)
        # copy the image to the GUI state, but screen might not changed yet
        fig.canvas.blit(fig.bbox)
        # flush any pending GUI events, re-painting the screen if needed
        fig.canvas.flush_events()

    # Let the event loop process everything before leaving
    plt.pause(0.1)

