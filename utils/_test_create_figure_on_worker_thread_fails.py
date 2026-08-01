
def _test_create_figure_on_worker_thread_fails():
    def create_figure():
        warn_msg = "Matplotlib GUI outside of the main thread will likely fail."
        err_msg = "Cannot create a GUI FigureManager outside the main thread"
        with pytest.warns(UserWarning, match=warn_msg):
            with pytest.raises(RuntimeError, match=err_msg):
                plt.gcf()

    worker = threading.Thread(target=create_figure)
    worker.start()
    worker.join()

