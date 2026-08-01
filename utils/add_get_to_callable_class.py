
def add_get_to_callable_class(builder: IRBuilder, fn_info: FuncInfo) -> None:
    """Generate the '__get__' method for a callable class."""
    line = fn_info.fitem.line
    with builder.enter_method(
        fn_info.callable_class.ir,
        "__get__",
        object_rprimitive,
        fn_info,
        self_type=object_rprimitive,
    ):
        instance = builder.add_argument("instance", object_rprimitive)
        builder.add_argument("owner", object_rprimitive)

        # If accessed through the class, just return the callable
        # object. If accessed through an object, create a new bound
        # instance method object.
        instance_block, class_block = BasicBlock(), BasicBlock()
        comparison = builder.translate_is_op(
            builder.read(instance), builder.none_object(line), "is", line
        )
        builder.add_bool_branch(comparison, class_block, instance_block)

        builder.activate_block(class_block)
        builder.add(Return(builder.self()))

        builder.activate_block(instance_block)
        builder.add(
            Return(builder.call_c(method_new_op, [builder.self(), builder.read(instance)], line))
        )

