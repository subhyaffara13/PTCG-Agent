
def transform_lambda_expr(builder: IRBuilder, expr: LambdaExpr) -> Value:
    typ = get_proper_type(builder.types[expr])
    assert isinstance(typ, CallableType), typ

    runtime_args = []
    for arg, arg_type in zip(expr.arguments, typ.arg_types):
        arg.variable.type = arg_type
        runtime_args.append(
            RuntimeArg(arg.variable.name, builder.type_to_rtype(arg_type), arg.kind)
        )
    ret_type = builder.type_to_rtype(typ.ret_type)

    fsig = FuncSignature(runtime_args, ret_type)

    fname = f"{LAMBDA_NAME}{builder.lambda_counter}"
    builder.lambda_counter += 1
    func_ir, func_reg = gen_func_item(builder, expr, fname, fsig)
    assert func_reg is not None

    builder.functions.append(func_ir)
    return func_reg

