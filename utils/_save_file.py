
def _save_file(pickler, obj, open_):
    if obj.closed:
        position = 0
    else:
        obj.flush()
        if obj in (sys.__stdout__, sys.__stderr__, sys.__stdin__):
            position = -1
        else:
            position = obj.tell()
    if is_dill(pickler, child=True) and pickler._fmode == FILE_FMODE:
        f = open_(obj.name, "r")
        fdata = f.read()
        f.close()
    else:
        fdata = ""
    if is_dill(pickler, child=True):
        strictio = pickler._strictio
        fmode = pickler._fmode
    else:
        strictio = False
        fmode = 0 # HANDLE_FMODE
    pickler.save_reduce(_create_filehandle, (obj.name, obj.mode, position,
                                             obj.closed, open_, strictio,
                                             fmode, fdata), obj=obj)
    return

