
def add_docstr_all(method: str, docstr: str) -> None:
    add_docstr(getattr(torch._C.Size, method), docstr)


def add_docstr_all(method, docstr):
    for cls_name in storage_classes:
        cls = getattr(torch._C, cls_name)
        try:
            add_docstr(getattr(cls, method), docstr)
        except AttributeError:
            pass


def add_docstr_all(method: str, docstr: str) -> None:
    add_docstr(getattr(torch._C.TensorBase, method), docstr)

