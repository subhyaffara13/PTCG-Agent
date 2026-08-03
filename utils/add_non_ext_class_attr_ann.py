from typing import Callable

def add_non_ext_class_attr_ann(
    builder: IRBuilder,
    non_ext: NonExtClassInfo,
    lvalue: NameExpr,
    stmt: AssignmentStmt,
    get_type_info: Callable[[AssignmentStmt], TypeInfo | None] | None = None,
) -> None:
    """Add a class attribute to __annotations__ of a non-extension class."""
    # FIXME: try to better preserve the special forms and type parameters of generics.
    typ: Value | None = None
    if get_type_info is not None:
        type_info = get_type_info(stmt)
        if type_info:
            # NOTE: Using string type information is similar to using
            # `from __future__ import annotations` in standard python.
            # NOTE: For string types we need to use the fullname since it
            # includes the module. If string type doesn't have the module,
            # @dataclass will try to get the current module and fail since the
            # current module is not in sys.modules.
            if builder.current_module == type_info.module_name and stmt.line < type_info.line:
                typ = builder.load_str(type_info.fullname)
            else:
                typ = load_type(builder, type_info, stmt.unanalyzed_type, stmt.line)

    if typ is None:
        # FIXME: if get_type_info is not provided, don't fall back to stmt.type?
        ann_type = get_proper_type(stmt.type)
        if (
            isinstance(stmt.unanalyzed_type, UnboundType)
            and stmt.unanalyzed_type.original_str_expr is not None
        ):
            # Annotation is a forward reference, so don't attempt to load the actual
            # type and load the string instead.
            #
            # TODO: is it possible to determine whether a non-string annotation is
            # actually a forward reference due to the __annotations__ future?
            typ = builder.load_str(stmt.unanalyzed_type.original_str_expr)
        elif isinstance(ann_type, Instance):
            typ = load_type(builder, ann_type.type, stmt.unanalyzed_type, stmt.line)
        else:
            typ = builder.add(LoadAddress(type_object_op.type, type_object_op.src, stmt.line))

    key = builder.load_str(lvalue.name)
    builder.call_c(exact_dict_set_item_op, [non_ext.anns, key, typ], stmt.line)

