
def _test_thread_impl():
    from concurrent.futures import ThreadPoolExecutor

    import matplotlib as mpl
    from matplotlib import pyplot as plt

    mpl.rcParams.update({
        "webagg.open_in_browser": False,
        "webagg.port_retries": 1,
    })

    # Test artist creation and drawing does not crash from thread
    # No other guarantees!
    fig, ax = plt.subplots()
    # plt.pause needed vs plt.show(block=False) at least on toolbar2-tkagg
    plt.pause(0.5)

    future = ThreadPoolExecutor().submit(ax.plot, [1, 3, 6])
    future.result()  # Joins the thread; rethrows any exception.

    fig.canvas.mpl_connect("close_event", print)
    future = ThreadPoolExecutor().submit(fig.canvas.draw)
    plt.pause(0.5)  # flush_events fails here on at least Tkagg (bpo-41176)
    future.result()  # Joins the thread; rethrows any exception.
    # stash the current canvas as closing the figure will reset the canvas on
    # the figure
    canvas = fig.canvas
    plt.close()  # backend is responsible for flushing any events here
    if plt.rcParams["backend"].lower().startswith("wx"):
        # TODO: debug why WX needs this only on py >= 3.8
        canvas.flush_events()

