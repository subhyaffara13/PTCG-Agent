
def frequently_executed_blocks(entry_point: BasicBlock) -> set[BasicBlock]:
    result: set[BasicBlock] = set()
    worklist = [entry_point]
    while worklist:
        block = worklist.pop()
        if block in result:
            continue
        result.add(block)
        t = block.terminator
        if isinstance(t, Goto):
            worklist.append(t.label)
        elif isinstance(t, Branch):
            if t.rare or t.traceback_entry is not None:
                worklist.append(t.false)
            else:
                worklist.append(t.true)
                worklist.append(t.false)
    return result

