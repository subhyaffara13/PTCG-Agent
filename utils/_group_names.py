
def _group_names(gns: list[BaseSchedulerNode]) -> str:
    return "~".join([gn.get_name() for gn in gns])

