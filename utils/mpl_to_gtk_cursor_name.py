
def mpl_to_gtk_cursor_name(mpl_cursor):
    return _api.getitem_checked({
        Cursors.MOVE: "move",
        Cursors.HAND: "pointer",
        Cursors.POINTER: "default",
        Cursors.SELECT_REGION: "crosshair",
        Cursors.WAIT: "wait",
        Cursors.RESIZE_HORIZONTAL: "ew-resize",
        Cursors.RESIZE_VERTICAL: "ns-resize",
    }, cursor=mpl_cursor)

