
def is_class_attr(name: str, klass: nodes.ClassDef) -> bool:
    try:
        klass.getattr(name)
        return True
    except astroid.NotFoundError:
        return False

