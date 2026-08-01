
def get_max_prio(anns: list[Annotation]) -> list[Annotation]:
    max_prio = max(a.priority for a in anns)
    return [a for a in anns if a.priority == max_prio]

