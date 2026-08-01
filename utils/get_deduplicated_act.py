
def get_deduplicated_act(act_mapping: dict[int, ir.IRNode]) -> list[ir.IRNode]:
    act_deduplicated = []
    act_deduplicated_name: OrderedSet[str] = OrderedSet()
    for act_idx in range(len(act_mapping.values())):
        act = act_mapping[act_idx]
        if act.get_name() not in act_deduplicated_name:
            act_deduplicated.append(act)
            act_deduplicated_name.add(act.get_name())
    return act_deduplicated

