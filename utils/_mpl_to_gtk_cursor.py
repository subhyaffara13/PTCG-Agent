
def _mpl_to_gtk_cursor(mpl_cursor):
    return Gdk.Cursor.new_from_name(
        Gdk.Display.get_default(),
        _backend_gtk.mpl_to_gtk_cursor_name(mpl_cursor))

