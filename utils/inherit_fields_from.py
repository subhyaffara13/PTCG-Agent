
def inherit_fields_from(parent_cls):
    def wrapper(child_cls):
        for k, v in parent_cls.__dict__.items():
            # copy fields that are not private and not overridden
            if not k.startswith("_") and k not in child_cls.__dict__:
                setattr(child_cls, k, v)
        return child_cls

    return wrapper

