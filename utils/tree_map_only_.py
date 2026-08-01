
def tree_map_only_(
    type_or_types_or_pred: type[T],
    /,
    func: Fn[T, Any],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> PyTree: ...


def tree_map_only_(
    type_or_types_or_pred: Type2[T, S],
    /,
    func: Fn2[T, S, Any],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> PyTree: ...


def tree_map_only_(
    type_or_types_or_pred: Type3[T, S, U],
    /,
    func: Fn3[T, S, U, Any],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> PyTree: ...


def tree_map_only_(
    type_or_types_or_pred: TypeAny,
    /,
    func: FnAny[Any],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> PyTree: ...


def tree_map_only_(
    type_or_types_or_pred: Callable[[Any], bool],
    /,
    func: FnAny[Any],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> PyTree: ...


def tree_map_only_(
    type_or_types_or_pred: TypeAny | Callable[[Any], bool],
    /,
    func: FnAny[Any],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> PyTree:
    return tree_map_(map_only(type_or_types_or_pred)(func), tree, is_leaf=is_leaf)


def tree_map_only_(
    type_or_types_or_pred: type[T],
    /,
    func: Fn[T, Any],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> PyTree: ...


def tree_map_only_(
    type_or_types_or_pred: Type2[T, S],
    /,
    func: Fn2[T, S, Any],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> PyTree: ...


def tree_map_only_(
    type_or_types_or_pred: Type3[T, S, U],
    /,
    func: Fn3[T, S, U, Any],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> PyTree: ...


def tree_map_only_(
    type_or_types_or_pred: TypeAny,
    /,
    func: FnAny[Any],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> PyTree: ...


def tree_map_only_(
    type_or_types_or_pred: Callable[[Any], bool],
    /,
    func: FnAny[Any],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> PyTree: ...


def tree_map_only_(
    type_or_types_or_pred: TypeAny | Callable[[Any], bool],
    /,
    func: FnAny[Any],
    tree: PyTree,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> PyTree:
    return tree_map_(map_only(type_or_types_or_pred)(func), tree, is_leaf=is_leaf)

