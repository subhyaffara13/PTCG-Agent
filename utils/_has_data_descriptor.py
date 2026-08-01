
def _has_data_descriptor(cls: nodes.ClassDef, attr: str) -> bool:
    attributes = cls.getattr(attr)
    for attribute in attributes:
        try:
            for inferred in attribute.infer():
                if isinstance(inferred, astroid.Instance):
                    try:
                        inferred.getattr("__get__")
                        inferred.getattr("__set__")
                    except astroid.NotFoundError:
                        continue
                    else:
                        return True
        except astroid.InferenceError:
            # Can't infer, avoid emitting a false positive in this case.
            return True
    return False

