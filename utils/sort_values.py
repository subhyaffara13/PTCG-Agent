
def sort_values(values: Collection[Op], blocks: list[BasicBlock]) -> list[Op]:
    if len(values) > 1:
        order = {}
        i = 0
        for block in blocks:
            for op in block.ops:
                order[op] = i
                i += 1
        return sorted(values, key=lambda v: order[v])
    else:
        return list(values)

