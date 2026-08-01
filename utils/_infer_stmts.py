
def _infer_stmts(
    stmts: Iterable[InferenceResult],
    context: InferenceContext | None,
    frame: nodes.NodeNG | BaseInstance | None = None,
) -> collections.abc.Generator[InferenceResult]:
    """Return an iterator on statements inferred by each statement in *stmts*."""
    inferred = False
    constraint_failed = False
    if context is not None:
        name = context.lookupname
        context = context.clone()
        if name is not None:
            constraints = context.constraints.get(name, {})
        else:
            constraints = {}
    else:
        name = None
        constraints = {}
        context = InferenceContext()

    for stmt in stmts:
        if isinstance(stmt, UninferableBase):
            yield stmt
            inferred = True
            continue
        context.lookupname = stmt._infer_name(frame, name)
        try:
            stmt_constraints: set[Constraint] = set()
            for constraint_stmt, potential_constraints in constraints.items():
                if not constraint_stmt.parent_of(stmt):
                    stmt_constraints.update(potential_constraints)
            for inf in stmt.infer(context=context):
                if all(constraint.satisfied_by(inf) for constraint in stmt_constraints):
                    yield inf
                    inferred = True
                else:
                    constraint_failed = True
        except NameInferenceError:
            continue
        except InferenceError:
            yield Uninferable
            inferred = True

    if not inferred and constraint_failed:
        yield Uninferable
    elif not inferred:
        raise InferenceError(
            "Inference failed for all members of {stmts!r}.",
            stmts=stmts,
            frame=frame,
            context=context,
        )

