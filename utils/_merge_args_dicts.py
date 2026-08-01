
def _merge_args_dicts(args_classes_tuple: tuple) -> dict:
    """Cached merger of args-doc dicts. The input classes are static so caching is safe."""
    result = {}
    for cls in args_classes_tuple:
        result.update(cls.__dict__)
    return result

