
def is_object_or_named_tuple(checker, instance):
    if Draft202012Validator.TYPE_CHECKER.is_type(instance, "object"):
        return True
    return is_namedtuple(instance)

