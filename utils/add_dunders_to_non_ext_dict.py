
def add_dunders_to_non_ext_dict(
    builder: IRBuilder, non_ext: NonExtClassInfo, line: int, add_annotations: bool = True
) -> None:
    if add_annotations:
        # Add __annotations__ to the class dict.
        builder.add_to_non_ext_dict(non_ext, "__annotations__", non_ext.anns, line)

    # We add a __doc__ attribute so if the non-extension class is decorated with the
    # dataclass decorator, dataclass will not try to look for __text_signature__.
    # https://github.com/python/cpython/blob/3.7/Lib/dataclasses.py#L957
    filler_doc_str = "mypyc filler docstring"
    builder.add_to_non_ext_dict(non_ext, "__doc__", builder.load_str(filler_doc_str), line)
    builder.add_to_non_ext_dict(non_ext, "__module__", builder.load_str(builder.module_name), line)

