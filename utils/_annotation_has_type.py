
def _annotation_has_type(*, typ, annotation):
    if hasattr(annotation, "__args__"):
        for a in annotation.__args__:
            if _annotation_has_type(typ=typ, annotation=a):
                return True
        return False

    return typ is annotation

