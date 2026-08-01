
def _container_getitem(instance, elts, index, context: InferenceContext | None = None):
    """Get a slice or an item, using the given *index*, for the given sequence."""
    try:
        if isinstance(index, Slice):
            index_slice = _infer_slice(index, context=context)
            new_cls = instance.__class__()
            new_cls.elts = elts[index_slice]
            new_cls.parent = instance.parent
            return new_cls
        if isinstance(index, Const):
            return elts[index.value]
    except ValueError as exc:
        raise AstroidValueError(
            message="Slice {index!r} cannot index container",
            node=instance,
            index=index,
            context=context,
        ) from exc
    except IndexError as exc:
        raise AstroidIndexError(
            message="Index {index!s} out of range",
            node=instance,
            index=index,
            context=context,
        ) from exc
    except TypeError as exc:
        raise AstroidTypeError(
            message="Type error {error!r}", node=instance, index=index, context=context
        ) from exc

    raise AstroidTypeError(f"Could not use {index} as subscript index")

