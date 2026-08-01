
def transform_del_item(builder: IRBuilder, target: AssignmentTarget, line: int) -> None:
    if isinstance(target, AssignmentTargetIndex):
        builder.gen_method_call(
            target.base, "__delitem__", [target.index], result_type=None, line=line
        )
    elif isinstance(target, AssignmentTargetAttr):
        if isinstance(target.obj_type, RInstance):
            cl = target.obj_type.class_ir
            if not cl.is_deletable(target.attr):
                builder.error(f'"{target.attr}" cannot be deleted', line)
                builder.note(
                    'Using "__deletable__ = '
                    + '[\'<attr>\']" in the class body enables "del obj.<attr>"',
                    line,
                )
        key = builder.load_str(target.attr)
        builder.primitive_op(py_delattr_op, [target.obj, key], line)
    elif isinstance(target, AssignmentTargetRegister):
        # Delete a local by assigning an error value to it, which will
        # prompt the insertion of uninit checks.
        builder.add(
            Assign(target.register, builder.add(LoadErrorValue(target.type, undefines=True)))
        )
    elif isinstance(target, AssignmentTargetTuple):
        for subtarget in target.items:
            transform_del_item(builder, subtarget, line)

