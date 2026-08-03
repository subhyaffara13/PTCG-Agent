import os

def test_save_figure_return():
    from gi.repository import Gtk
    fig, ax = plt.subplots()
    ax.imshow([[1]])
    with mock.patch("gi.repository.Gtk.FileFilter") as fileFilter:
        filt = fileFilter.return_value
        filt.get_name.return_value = "Portable Network Graphics"
        with mock.patch("gi.repository.Gtk.FileChooserDialog") as dialogChooser:
            dialog = dialogChooser.return_value
            dialog.get_filter.return_value = filt
            dialog.get_filename.return_value = "foobar.png"
            dialog.run.return_value = Gtk.ResponseType.OK
            fname = fig.canvas.manager.toolbar.save_figure()
            os.remove("foobar.png")
            assert fname == "foobar.png"

            with mock.patch("gi.repository.Gtk.MessageDialog"):
                dialog.get_filename.return_value = None
                dialog.run.return_value = Gtk.ResponseType.OK
                fname = fig.canvas.manager.toolbar.save_figure()
                assert fname is None


def test_save_figure_return():
    subprocess_run_helper(_test_save_figure_return, timeout=_test_timeout,
                          extra_env={"MPLBACKEND": "macosx"})


def test_save_figure_return(tmp_path):
    fig, ax = plt.subplots()
    ax.imshow([[1]])
    expected = tmp_path / "foobar.png"
    prop = "matplotlib.backends.qt_compat.QtWidgets.QFileDialog.getSaveFileName"
    with mock.patch(prop, return_value=(str(expected), None)):
        fname = fig.canvas.manager.toolbar.save_figure()
        assert fname == str(expected)
        assert expected.exists()
    with mock.patch(prop, return_value=(None, None)):
        fname = fig.canvas.manager.toolbar.save_figure()
        assert fname is None


def test_save_figure_return():
    import matplotlib.pyplot as plt
    from unittest import mock
    fig = plt.figure()
    prop = "tkinter.filedialog.asksaveasfilename"
    with mock.patch(prop, return_value="foobar.png"):
        fname = fig.canvas.manager.toolbar.save_figure()
        os.remove("foobar.png")
        assert fname == "foobar.png"
        print("success")
    with mock.patch(prop, return_value=""):
        fname = fig.canvas.manager.toolbar.save_figure()
        assert fname is None
        print("success")

