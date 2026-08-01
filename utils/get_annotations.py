
def get_annotations(obj):
    # In Python-3.10+ it is recommended to use inspect.get_annotations
    # See https://docs.python.org/3.10/howto/annotations.html
    # But also, in 3.10 annotations from base class are not inherited
    # by unannotated derived one, so they must be manually extracted
    annotations = inspect.get_annotations(obj)
    if annotations:
        return annotations

    def get_cls_annotations(cls):
        cls_annotations = inspect.get_annotations(cls)
        if cls_annotations:
            return cls_annotations
        for base in cls.__bases__:
            cls_annotations = get_cls_annotations(base)
            if cls_annotations:
                return cls_annotations
        return {}

    cls = obj if isinstance(obj, type) else type(obj)
    return get_cls_annotations(cls)

