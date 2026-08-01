
def is_edit_valid(edit):
    text = edit.text()
    state = edit.validator().validate(text, 0)[0]
    return state == QtGui.QDoubleValidator.State.Acceptable

