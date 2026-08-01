
def test_figuremanager_cleans_own_mainloop():
    import tkinter
    import time
    import matplotlib.pyplot as plt
    import threading
    from matplotlib.cbook import _get_running_interactive_framework

    root = tkinter.Tk()
    plt.plot([1, 2, 3], [1, 2, 5])

    def target():
        while not 'tk' == _get_running_interactive_framework():
            time.sleep(.01)
        plt.close()
        if show_finished_event.wait():
            print('success')

    show_finished_event = threading.Event()
    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    plt.show(block=True)  # Testing if this function hangs.
    show_finished_event.set()
    thread.join()

