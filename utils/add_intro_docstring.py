
def add_intro_docstring(func, class_name, indent_level=0):
    intro_docstring = ""
    if func.__name__ == "forward":
        intro_docstring = rf"""The [`{class_name}`] forward method, overrides the `__call__` special method.

        <Tip>

        Although the recipe for forward pass needs to be defined within this function, one should call the [`Module`]
        instance afterwards instead of this since the former takes care of running the pre and post processing steps while
        the latter silently ignores them.

        </Tip>

        """
        intro_docstring = equalize_indent(intro_docstring, indent_level + 4)

    return intro_docstring

