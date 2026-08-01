
def is_pybind11_overloaded_function_docstring(docstring: str, name: str) -> bool:
    return docstring.startswith(f"{name}(*args, **kwargs)\nOverloaded function.\n\n")

