
def get_real_target(label: BasicBlock) -> BasicBlock:
    if len(label.ops) == 1 and isinstance(label.ops[-1], Goto):
        label = label.ops[-1].label
    return label

