
def move_code_under_inner_loop(
    code: IndentedBuffer,
    iter_var: sympy.Expr,
    new_iter_var: str,
    loop_start: sympy.Expr,
    loop_end: sympy.Expr,
) -> BracesBuffer:
    r"""
    f(iter_var) is transformed to f(new_iter_var) under the inner loop
      \/
    for (new_iter_var = loop_start; new_iter_var < loop_end; new_iter_var++) {
        f(new_iter_var)
    }
    Please be careful while using this function,
    as the variable defined in f(iter_var) will be invalid outside the for loop.
    For example:
    auto tmp0 = in_ptr[x0]; ->
    for (new_x0 = start; new_x0 < end; new_x0++){
        auto tmp0 = in_ptr[new_x0];
    }
    The tmp0 is invalid outside the loop.
    """
    transformed_code = BracesBuffer()
    with contextlib.ExitStack() as stack:
        transformed_code.writeline(
            f"for ({INDEX_TYPE} {new_iter_var} = {cexpr_index(loop_start)};"
            + f"{new_iter_var} < {cexpr_index(loop_end)}; {new_iter_var}++)"
        )
        stack.enter_context(transformed_code.indent())
        for _, line in enumerate(code._lines):
            assert isinstance(
                line,
                (
                    str,
                    DeferredLine,
                ),
            )
            deferred_name = None
            if isinstance(line, DeferredLine):
                deferred_name = line.name
                line = line.line
            new_line = re.sub(r"\b" + f"{iter_var}" + r"\b", f"{new_iter_var}", line)
            if deferred_name:
                new_line = DeferredLine(deferred_name, new_line)  # type: ignore[assignment]
            transformed_code.writeline(new_line)
    return transformed_code

