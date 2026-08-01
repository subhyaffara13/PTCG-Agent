
def native_function_doc_initializer(func: FuncIR) -> str:
    text_sig = get_text_signature(func)
    if text_sig is None:
        return "NULL"
    docstring = f"{text_sig}\n--\n\n"
    return c_string_initializer(docstring.encode("ascii", errors="backslashreplace"))

