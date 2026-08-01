
def _weakref_handle(info: "tuple[weakref.ref[object], str]") -> None:
    ref, name = info
    ob = ref()
    if ob is not None:
        with suppress(Exception):
            getattr(ob, name)()

