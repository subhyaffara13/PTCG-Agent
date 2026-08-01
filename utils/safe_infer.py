
def safe_infer(
    node: nodes.NodeNG | bases.Proxy | util.UninferableBase,
    context: InferenceContext | None = None,
) -> InferenceResult | None:
    # When removing, also remove the real_safe_infer alias
    warnings.warn(
        "Import safe_infer from astroid.util; this shim in astroid.helpers will be removed.",
        DeprecationWarning,
        stacklevel=2,
    )
    return real_safe_infer(node, context=context)


def safe_infer(
    node: nodes.NodeNG | bases.Proxy | UninferableBase,
    context: InferenceContext | None = None,
) -> InferenceResult | None:
    """Return the inferred value for the given node.

    Return None if inference failed or if there is some ambiguity (more than
    one node has been inferred).
    """
    if isinstance(node, UninferableBase):
        return node
    try:
        inferit = node.infer(context=context)
        value = next(inferit)
    except (InferenceError, StopIteration):
        return None
    try:
        next(inferit)
        return None  # None if there is ambiguity on the inferred node
    except InferenceError:
        return None  # there is some kind of ambiguity
    except StopIteration:
        return value


def safe_infer(
    node: nodes.NodeNG,
    context: InferenceContext | None = None,
    *,
    compare_constants: bool = False,
    compare_constructors: bool = False,
) -> InferenceResult | None:
    """Return the inferred value for the given node.

    Return None if inference failed or if there is some ambiguity (more than
    one node has been inferred of different types).

    If compare_constants is True and if multiple constants are inferred,
    unequal inferred values are also considered ambiguous and return None.

    If compare_constructors is True and if multiple classes are inferred,
    constructors with different signatures are held ambiguous and return None.
    """
    inferred_types: set[str | None] = set()
    try:
        infer_gen = node.infer(context=context)
        value = next(infer_gen)
    except astroid.InferenceError:
        return None
    except Exception as e:  # pragma: no cover
        raise AstroidError from e

    if not isinstance(value, util.UninferableBase):
        inferred_types.add(_get_python_type_of_node(value))

    # pylint: disable = too-many-try-statements
    try:
        for inferred in infer_gen:
            inferred_type = _get_python_type_of_node(inferred)
            if inferred_type not in inferred_types:
                return None  # If there is ambiguity on the inferred node.
            if (
                compare_constants
                and isinstance(inferred, nodes.Const)
                and isinstance(value, nodes.Const)
                and inferred.value != value.value
            ):
                return None
            if (
                isinstance(inferred, nodes.FunctionDef)
                and isinstance(value, nodes.FunctionDef)
                and function_arguments_are_ambiguous(inferred, value)
            ):
                return None
            if (
                compare_constructors
                and isinstance(inferred, nodes.ClassDef)
                and isinstance(value, nodes.ClassDef)
                and class_constructors_are_ambiguous(inferred, value)
            ):
                return None
    except astroid.InferenceError:
        return None  # There is some kind of ambiguity
    except StopIteration:
        return value
    except Exception as e:  # pragma: no cover
        raise AstroidError from e
    return value if len(inferred_types) <= 1 else None

