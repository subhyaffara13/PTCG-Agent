
def native_class_doc_initializer(cl: ClassIR) -> str:
    init_fn = cl.get_method("__init__")
    if init_fn is not None:
        text_sig = get_text_signature(init_fn, bound=True)
        if text_sig is None:
            return "NULL"
        text_sig = text_sig.replace("__init__", cl.name, 1)
    else:
        text_sig = f"{cl.name}()"
    docstring = f"{text_sig}\n--\n\n"
    return c_string_initializer(docstring.encode("ascii", errors="backslashreplace"))

