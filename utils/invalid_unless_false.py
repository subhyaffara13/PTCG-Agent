
def invalid_unless_false(dist, attr, value):
    if not value:
        DistDeprecationWarning.emit(f"{attr} is ignored.")
        # TODO: should there be a `due_date` here?
        return
    raise DistutilsSetupError(f"{attr} is invalid.")

