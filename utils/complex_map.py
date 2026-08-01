
def complex_map(xs, ys):
    """Returns a 2D 'map' with a four different obstacles.

    Map is a 2D numpy array
    """
    cmap = np.zeros((xs, ys), dtype=np.int32)
    cmap = add_rectangle(cmap, xc=0.8, yc=0.5, xl=0.1, yl=0.8)
    cmap = add_rectangle(cmap, xc=0.4, yc=0.8, xl=0.5, yl=0.2)
    cmap = add_rectangle(cmap, xc=0.5, yc=0.5, xl=0.4, yl=0.2)
    cmap = add_rectangle(cmap, xc=0.3, yc=0.1, xl=0.5, yl=0.1)
    cmap = add_rectangle(cmap, xc=0.1, yc=0.3, xl=0.1, yl=0.5)
    return cmap

