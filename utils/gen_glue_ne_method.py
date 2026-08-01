
def gen_glue_ne_method(builder: IRBuilder, cls: ClassIR, line: int) -> None:
    """Generate a "__ne__" method from a "__eq__" method."""
    eq_sig = cls.method_sig("__eq__")
    strict_typing = builder.options.strict_dunders_typing
    with builder.enter_method(cls, "__ne__", eq_sig.ret_type):
        rhs_type = eq_sig.args[1].type
        rhs_arg = builder.add_argument("rhs", rhs_type)
        eqval = builder.add(MethodCall(builder.self(), "__eq__", [rhs_arg], line))

        can_return_not_implemented = is_subtype(not_implemented_op.type, eq_sig.ret_type)
        return_bool = is_subtype(eq_sig.ret_type, bool_rprimitive)

        if not strict_typing or can_return_not_implemented:
            # If __eq__ returns NotImplemented, then __ne__ should also
            not_implemented_block, regular_block = BasicBlock(), BasicBlock()
            not_implemented = builder.add(
                LoadAddress(not_implemented_op.type, not_implemented_op.src, line)
            )
            builder.add(
                Branch(
                    builder.translate_is_op(eqval, not_implemented, "is", line),
                    not_implemented_block,
                    regular_block,
                    Branch.BOOL,
                )
            )
            builder.activate_block(regular_block)
            rettype = bool_rprimitive if return_bool and strict_typing else object_rprimitive
            retval = builder.coerce(
                builder.builder.unary_not(eqval, line, likely_bool=True), rettype, line
            )
            builder.add(Return(retval))
            builder.activate_block(not_implemented_block)
            builder.add(Return(not_implemented))
        else:
            rettype = bool_rprimitive if return_bool and strict_typing else object_rprimitive
            retval = builder.coerce(builder.unary_op(eqval, "not", line), rettype, line)
            builder.add(Return(retval))

