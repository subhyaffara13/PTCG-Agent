
def test_blit():
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.backends.backend_tkagg  # noqa
    from matplotlib.backends import _backend_tk, _tkagg

    fig, ax = plt.subplots()
    photoimage = fig.canvas._tkphoto
    data = np.ones((4, 4, 4), dtype=np.uint8)
    # Test out of bounds blitting.
    bad_boxes = ((-1, 2, 0, 2),
                 (2, 0, 0, 2),
                 (1, 6, 0, 2),
                 (0, 2, -1, 2),
                 (0, 2, 2, 0),
                 (0, 2, 1, 6))
    for bad_box in bad_boxes:
        try:
            _tkagg.blit(
                photoimage.tk.interpaddr(), str(photoimage), data,
                _tkagg.TK_PHOTO_COMPOSITE_OVERLAY, (0, 1, 2, 3), bad_box)
        except ValueError:
            print("success")

    # Test blitting to a destroyed canvas.
    plt.close(fig)
    _backend_tk.blit(photoimage, data, (0, 1, 2, 3))

