
def _tree_map_with_path(
    func: Callable[..., Any],
    tree: Any,
    *dynamic_shapes: Any,
    tree_name: str | None = None,
) -> Any:
    """
    Customized tree_map for mapping pytrees to dynamic_shapes.

    For built-in types (e.g., standard collections) this behaves exactly like tree_map.

    OTOH for a user-defined class C registered with pytree, we cannot assume that a C
    containing tensors can be mapped to a C containing dynamic shapes (i.e., C may not
    be a polymorphic container). In that case we use the flattened form of C instead.
    Thus a C(**tensors) that flattens to (**tensors) will map to (**dynamic_shapes).

    Args:
        func: function to apply to each (int, float, str, bool, None, torch.Tensor)
        tree: input pytree
        dynamic_shapes: zero or more (typically one) dynamic_shapes to match

    Returns:
        output pytree mapping func to each (int, float, str, bool, None, torch.Tensor)
    """

    def is_leaf(t):
        # BUILTIN_TYPES is a subset of SUPPORTED_NODES, the latter being all types
        # registered with pytree. Types *not* in BUILTIN_TYPES include primitive types
        # (int, float, str, bool, None, torch.Tensor), which are not in SUPPORTED_NODES,
        # as well as user-defined classes registered with pytree, which are.
        return _get_node_type(t) not in BUILTIN_TYPES

    def f(path, t, *dynamic_shapes):
        typ = _get_node_type(t)
        # typ is not in BUILTIN_TYPES
        if typ in SUPPORTED_NODES:
            # thus typ is a user-defined class registered with pytree,
            # in which case flatten and recurse
            return tree_map_with_path(
                f,
                SUPPORTED_NODES[typ].flatten_fn(t)[0],
                *dynamic_shapes,
                is_leaf=is_leaf,
            )
        else:
            return func(path, t, *dynamic_shapes)

    try:
        return tree_map_with_path(f, tree, *dynamic_shapes, is_leaf=is_leaf)
    except ValueError as e:
        if "mismatch" in e.args[0]:
            # When PyTree finds a structural mismatch between tree and dynamic_shapes,
            # the error message is unfortunately quite horrible. Let's fix that.
            if not dynamic_shapes:
                raise AssertionError(
                    "Cannot be a mismatch if there is no dynamic_shapes"
                ) from None
            if not tree_name:
                raise AssertionError(
                    "Must provide a tree_name when there might be a mismatch"
                ) from None

            def _key(type_, context, i):
                # derive a PyTree key given the type, context, and child # of a TreeSpec
                if type_ is dict:
                    return MappingKey(context[i])
                if type_ in (list, tuple):
                    if context is not None:
                        raise AssertionError(
                            f"expected context to be None for type {type_}, got {context}"
                        )
                    return SequenceKey(i)
                raise AssertionError(f"Did not expect type {type_}")

            def raise_mismatch_error(msg):
                from torch._dynamo.exc import UserError, UserErrorType

                raise UserError(
                    UserErrorType.INVALID_INPUT,
                    f"Detected mismatch between the structure of `{tree_name}` and `dynamic_shapes`: {msg}",
                    case_name="dynamic_shapes_validation",
                )

            def _compare(
                treespec: TreeSpec, other_treespec: TreeSpec, path: KeyPath
            ) -> None:
                # raise an error at the point where tree and dynamic_shapes differ,
                # including the path to that point and the reason for the difference
                rendered_path = keystr(path)
                if treespec.is_leaf():
                    return
                if other_treespec.is_leaf():
                    raise_mismatch_error(
                        f"`{tree_name}{rendered_path}` is a {treespec.type}, "
                        f"but `dynamic_shapes{rendered_path}` is not"
                    )
                if treespec.type != other_treespec.type:
                    raise_mismatch_error(
                        f"`{tree_name}{rendered_path}` is a {treespec.type}, "
                        f"but `dynamic_shapes{rendered_path}` is a {other_treespec.type}"
                    )
                if treespec.num_children != other_treespec.num_children:
                    raise_mismatch_error(
                        f"`{tree_name}{rendered_path}` has {treespec.num_children} elements, "
                        f"but `dynamic_shapes{rendered_path}` has {other_treespec.num_children} elements"
                    )
                if treespec.type is dict:
                    # context, children could be out of order
                    if set(treespec.context) != set(other_treespec.context):
                        raise_mismatch_error(
                            f"`{tree_name}{rendered_path}` has keys {treespec.context}, "
                            f"but `dynamic_shapes{rendered_path}` has keys {other_treespec.context}"
                        )
                    _remap = dict(
                        zip(other_treespec.context, other_treespec.children())
                    )
                    other_children = [_remap[k] for k in treespec.context]
                else:
                    other_children = other_treespec.children()
                for i, (child, other_child) in enumerate(
                    zip(treespec.children(), other_children)
                ):
                    _compare(
                        child,
                        other_child,
                        path + (_key(treespec.type, treespec.context, i),),
                    )

            treespec = tree_structure(tree, is_leaf=is_leaf)
            for other_tree in dynamic_shapes:
                other_treespec = tree_structure(other_tree, is_leaf)
                _compare(treespec, other_treespec, ())
        raise

