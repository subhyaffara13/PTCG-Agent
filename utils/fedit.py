
def fedit(data, title="", comment="", icon=None, parent=None, apply=None):
    """
    Create form dialog

    data: datalist, datagroup
    title: str
    comment: str
    icon: QIcon instance
    parent: parent QWidget
    apply: apply callback (function)

    datalist: list/tuple of (field_name, field_value)
    datagroup: list/tuple of (datalist *or* datagroup, title, comment)

    -> one field for each member of a datalist
    -> one tab for each member of a top-level datagroup
    -> one page (of a multipage widget, each page can be selected with a combo
       box) for each member of a datagroup inside a datagroup

    Supported types for field_value:
      - int, float, str, bool
      - colors: in Qt-compatible text form, i.e. in hex format or name
                (red, ...) (automatically detected from a string)
      - list/tuple:
          * the first element will be the selected index (or value)
          * the other elements can be couples (key, value) or only values
    """

    # Create a QApplication instance if no instance currently exists
    # (e.g., if the module is used directly from the interpreter)
    if QtWidgets.QApplication.startingUp():
        _app = QtWidgets.QApplication([])
    dialog = FormDialog(data, title, comment, icon, parent, apply)

    if parent is not None:
        if hasattr(parent, "_fedit_dialog"):
            parent._fedit_dialog.close()
        parent._fedit_dialog = dialog

    dialog.show()

