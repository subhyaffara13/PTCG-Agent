
def add_start_docstrings_to_model_forward(*docstr):
    def docstring_decorator(fn):
        class_name = f"[`{fn.__qualname__.split('.')[0]}`]"
        intro = rf"""    The {class_name} forward method, overrides the `__call__` special method.

    <Tip>

    Although the recipe for forward pass needs to be defined within this function, one should call the [`Module`]
    instance afterwards instead of this since the former takes care of running the pre and post processing steps while
    the latter silently ignores them.

    </Tip>
"""

        correct_indentation = get_docstring_indentation_level(fn)
        current_doc = fn.__doc__ if fn.__doc__ is not None else ""
        try:
            first_non_empty = next(line for line in current_doc.splitlines() if line.strip() != "")
            doc_indentation = len(first_non_empty) - len(first_non_empty.lstrip())
        except StopIteration:
            doc_indentation = correct_indentation

        docs = docstr
        # In this case, the correct indentation level (class method, 2 Python levels) was respected, and we should
        # correctly reindent everything. Otherwise, the doc uses a single indentation level
        if doc_indentation == 4 + correct_indentation:
            docs = [textwrap.indent(textwrap.dedent(doc), " " * correct_indentation) for doc in docstr]
            intro = textwrap.indent(textwrap.dedent(intro), " " * correct_indentation)

        docstring = "".join(docs) + current_doc
        fn.__doc__ = intro + docstring
        return fn

    return docstring_decorator

