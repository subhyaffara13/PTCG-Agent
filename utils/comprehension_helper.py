
def comprehension_helper(
    builder: IRBuilder,
    loop_params: list[tuple[Lvalue, Expression, list[Expression], bool]],
    gen_inner_stmts: Callable[[], None],
    line: int,
) -> None:
    """Helper function for list comprehensions.

    Args:
        loop_params: a list of (index, expr, [conditions]) tuples defining nested loops:
            - "index" is the Lvalue indexing that loop;
            - "expr" is the expression for the object to be iterated over;
            - "conditions" is a list of conditions, evaluated in order with short-circuiting,
                that must all be true for the loop body to be executed
        gen_inner_stmts: function to generate the IR for the body of the innermost loop
    """

    def handle_loop(loop_params: list[tuple[Lvalue, Expression, list[Expression], bool]]) -> None:
        """Generate IR for a loop.

        Given a list of (index, expression, [conditions]) tuples, generate IR
        for the nested loops the list defines.
        """
        index, expr, conds, is_async = loop_params[0]
        for_loop_helper(
            builder,
            index,
            expr,
            lambda: loop_contents(conds, loop_params[1:]),
            None,
            is_async=is_async,
            line=line,
        )

    def loop_contents(
        conds: list[Expression],
        remaining_loop_params: list[tuple[Lvalue, Expression, list[Expression], bool]],
    ) -> None:
        """Generate the body of the loop.

        Args:
            conds: a list of conditions to be evaluated (in order, with short circuiting)
                to gate the body of the loop
            remaining_loop_params: the parameters for any further nested loops; if it's empty
                we'll instead evaluate the "gen_inner_stmts" function
        """
        # Check conditions, in order, short-circuiting them.
        for cond in conds:
            with builder.enter_borrow_scope(line):
                cond_val = builder.accept(cond)
            cont_block, rest_block = BasicBlock(), BasicBlock()
            # If the condition is true we'll skip the continue.
            builder.add_bool_branch(cond_val, rest_block, cont_block)
            builder.activate_block(cont_block)
            builder.nonlocal_control[-1].gen_continue(builder, cond.line)
            builder.goto_and_activate(rest_block)

        if remaining_loop_params:
            # There's another nested level, so the body of this loop is another loop.
            return handle_loop(remaining_loop_params)
        else:
            # We finally reached the actual body of the generator.
            # Generate the IR for the inner loop body.
            with builder.enter_borrow_scope(line):
                gen_inner_stmts()

    handle_loop(loop_params)

