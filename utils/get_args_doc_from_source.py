
def get_args_doc_from_source(args_classes: object | list[object]) -> dict:
    if isinstance(args_classes, list | tuple):
        return _merge_args_dicts(tuple(args_classes))
    return args_classes.__dict__

