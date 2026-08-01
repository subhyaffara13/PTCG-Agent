
def _test_threading():
    import threading
    from matplotlib.ft2font import LoadFlags
    import matplotlib.font_manager as fm

    def loud_excepthook(args):
        raise RuntimeError("error in thread!")

    threading.excepthook = loud_excepthook

    N = 10
    b = threading.Barrier(N)

    def bad_idea(n):
        b.wait(timeout=5)
        for j in range(100):
            font = fm.get_font(fm.findfont("DejaVu Sans"))
            font.set_text(str(n), 0.0, flags=LoadFlags.NO_HINTING)

    threads = [
        threading.Thread(target=bad_idea, name=f"bad_thread_{j}", args=(j,))
        for j in range(N)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join(timeout=9)
        if t.is_alive():
            raise RuntimeError("thread failed to join")

