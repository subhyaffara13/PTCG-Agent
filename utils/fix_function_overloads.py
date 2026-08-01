
def fix_function_overloads(state: State, stmts: list[Statement]) -> list[Statement]:
    """Merge consecutive function overloads into OverloadedFuncDef nodes.

    Also handles conditional overloads (overloads inside if statements).
    """
    ret: list[Statement] = []
    current_overload: list[OverloadPart] = []
    current_overload_name: str | None = None
    last_unconditional_func_def: str | None = None
    last_if_stmt: IfStmt | None = None
    last_if_overload: Decorator | FuncDef | OverloadedFuncDef | None = None
    last_if_stmt_overload_name: str | None = None
    last_if_unknown_truth_value: IfStmt | None = None
    skipped_if_stmts: list[IfStmt] = []
    for stmt in stmts:
        if_overload_name: str | None = None
        if_block_with_overload: Block | None = None
        if_unknown_truth_value: IfStmt | None = None
        if isinstance(stmt, IfStmt):
            # Check IfStmt block to determine if function overloads can be merged
            if_overload_name = check_ifstmt_for_overloads(stmt, current_overload_name)
            if if_overload_name is not None:
                if_block_with_overload, if_unknown_truth_value = (
                    get_executable_if_block_with_overloads(stmt, state.options)
                )

        if (
            current_overload_name is not None
            and isinstance(stmt, (Decorator, FuncDef))
            and stmt.name == current_overload_name
        ):
            if last_if_stmt is not None:
                skipped_if_stmts.append(last_if_stmt)
            if last_if_overload is not None:
                # Last stmt was an IfStmt with same overload name
                # Add overloads to current_overload
                if isinstance(last_if_overload, OverloadedFuncDef):
                    current_overload.extend(last_if_overload.items)
                else:
                    current_overload.append(last_if_overload)
                last_if_stmt, last_if_overload = None, None
            if last_if_unknown_truth_value:
                fail_merge_overload(state, last_if_unknown_truth_value)
                last_if_unknown_truth_value = None
            current_overload.append(stmt)
            if isinstance(stmt, FuncDef):
                # This is, strictly speaking, wrong: there might be a decorated
                # implementation. However, it only affects the error message we show:
                # ideally it's "already defined", but "implementation must come last"
                # is also reasonable.
                # TODO: can we get rid of this completely and just always emit
                # "implementation must come last" instead?
                last_unconditional_func_def = stmt.name
        elif (
            current_overload_name is not None
            and isinstance(stmt, IfStmt)
            and if_overload_name == current_overload_name
            and last_unconditional_func_def != current_overload_name
        ):
            # IfStmt only contains stmts relevant to current_overload.
            # Check if stmts are reachable and add them to current_overload,
            # otherwise skip IfStmt to allow subsequent overload
            # or function definitions.
            skipped_if_stmts.append(stmt)
            if if_block_with_overload is None:
                if if_unknown_truth_value is not None:
                    fail_merge_overload(state, if_unknown_truth_value)
                continue
            if last_if_overload is not None:
                # Last stmt was an IfStmt with same overload name
                # Add overloads to current_overload
                if isinstance(last_if_overload, OverloadedFuncDef):
                    current_overload.extend(last_if_overload.items)
                else:
                    current_overload.append(last_if_overload)
                last_if_stmt, last_if_overload = None, None
            if isinstance(if_block_with_overload.body[-1], OverloadedFuncDef):
                skipped_if_stmts.extend(cast(list[IfStmt], if_block_with_overload.body[:-1]))
                current_overload.extend(if_block_with_overload.body[-1].items)
            else:
                current_overload.append(cast(Decorator | FuncDef, if_block_with_overload.body[0]))
        else:
            if last_if_stmt is not None:
                ret.append(last_if_stmt)
                last_if_stmt_overload_name = current_overload_name
                last_if_stmt, last_if_overload = None, None
                last_if_unknown_truth_value = None

            if current_overload and current_overload_name == last_if_stmt_overload_name:
                # Remove last stmt (IfStmt) from ret if the overload names matched
                # Only happens if no executable block had been found in IfStmt
                popped = ret.pop()
                assert isinstance(popped, IfStmt)
                skipped_if_stmts.append(popped)
            if current_overload and skipped_if_stmts:
                # Add bare IfStmt (without overloads) to ret
                # Required for mypy to be able to still check conditions
                for if_stmt in skipped_if_stmts:
                    strip_contents_from_if_stmt(if_stmt)
                    ret.append(if_stmt)
                skipped_if_stmts = []
            if len(current_overload) == 1:
                ret.append(current_overload[0])
            elif len(current_overload) > 1:
                ret.append(OverloadedFuncDef(current_overload))

            # If we have multiple decorated functions named "_" next to each, we want to treat
            # them as a series of regular FuncDefs instead of one OverloadedFuncDef because
            # most of mypy/mypyc assumes that all the functions in an OverloadedFuncDef are
            # related, but multiple underscore functions next to each other aren't necessarily
            # related
            last_unconditional_func_def = None
            if isinstance(stmt, Decorator) and not unnamed_function(stmt.name):
                current_overload = [stmt]
                current_overload_name = stmt.name
            elif isinstance(stmt, IfStmt) and if_overload_name is not None:
                current_overload = []
                current_overload_name = if_overload_name
                last_if_stmt = stmt
                last_if_stmt_overload_name = None
                if if_block_with_overload is not None:
                    skipped_if_stmts.extend(cast(list[IfStmt], if_block_with_overload.body[:-1]))
                    last_if_overload = cast(
                        Decorator | FuncDef | OverloadedFuncDef, if_block_with_overload.body[-1]
                    )
                last_if_unknown_truth_value = if_unknown_truth_value
            else:
                current_overload = []
                current_overload_name = None
                ret.append(stmt)

    if current_overload and skipped_if_stmts:
        # Add bare IfStmt (without overloads) to ret
        # Required for mypy to be able to still check conditions
        for if_stmt in skipped_if_stmts:
            strip_contents_from_if_stmt(if_stmt)
            ret.append(if_stmt)
    if len(current_overload) == 1:
        ret.append(current_overload[0])
    elif len(current_overload) > 1:
        ret.append(OverloadedFuncDef(current_overload))
    elif last_if_overload is not None:
        ret.append(last_if_overload)
    elif last_if_stmt is not None:
        ret.append(last_if_stmt)
    return ret

