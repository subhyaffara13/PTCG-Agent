
def apply_plot(hist, hist_edges):
    import sys  # noqa: PLC0415

    import matplotlib.pyplot as plt  # noqa: PLC0415
    import numpy  # noqa: PLC0415

    numpy.set_printoptions(threshold=sys.maxsize)
    print("Histogram:")
    print(hist)
    print("Histogram Edges:")
    print(hist_edges)
    plt.stairs(hist, hist_edges, fill=True)
    plt.xlabel("Tensor value")
    plt.ylabel("Counts")
    plt.title("Tensor value V.S. Counts")
    plt.show()

