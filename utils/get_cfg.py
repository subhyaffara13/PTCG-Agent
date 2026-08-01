
def get_cfg(blocks: list[BasicBlock], *, use_yields: bool = False) -> CFG:
    """Calculate basic block control-flow graph.

    If use_yields is set, then we treat returns inserted by yields as gotos
    instead of exits.
    """
    succ_map = {}
    pred_map: dict[BasicBlock, list[BasicBlock]] = {}
    exits = set()
    for block in blocks:
        assert not any(
            isinstance(op, ControlOp) for op in block.ops[:-1]
        ), "Control-flow ops must be at the end of blocks"

        if use_yields and isinstance(block.terminator, Return) and block.terminator.yield_target:
            succ = [block.terminator.yield_target]
        else:
            succ = list(block.terminator.targets())
        if not succ:
            exits.add(block)

        # Errors can occur anywhere inside a block, which means that
        # we can't assume that the entire block has executed before
        # jumping to the error handler. In our CFG construction, we
        # model this as saying that a block can jump to its error
        # handler or the error handlers of any of its normal
        # successors (to represent an error before that next block
        # completes). This works well for analyses like "must
        # defined", where it implies that registers assigned in a
        # block may be undefined in its error handler, but is in
        # general not a precise representation of reality; any
        # analyses that require more fidelity must wait until after
        # exception insertion.
        for error_point in [block] + succ:
            if error_point.error_handler:
                succ.append(error_point.error_handler)

        succ_map[block] = succ
        pred_map[block] = []
    for prev, nxt in succ_map.items():
        for label in nxt:
            pred_map[label].append(prev)
    return CFG(succ_map, pred_map, exits)

