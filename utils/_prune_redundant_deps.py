
def _prune_redundant_deps(
    node: BaseSchedulerNode,
    name_to_fused_node: dict[str, BaseSchedulerNode],
    name_to_buf: dict[str, SchedulerBuffer],
) -> None:
    """
    Prunes weakdeps intended for mutation ordering
    on an upstream fused node if after fusion there is another dependency
    on the fused upstream node, making the weakdep redundant

    In essence this enforces an ordering on fusions. As fusions occur, weakdeps will
    be incrementally removed, enabling other fusions, ensuring they are fused in order.
    """
    name_to_dep_count: Counter[str] = collections.Counter()

    for dep in node.unmet_dependencies:
        if not isinstance(dep, WeakDep):
            op_name = name_to_buf[dep.name].defining_op_name()
            name_to_dep_count[name_to_fused_node[op_name].get_name()] += 1

    def should_prune(dep: Dep) -> bool:
        if isinstance(dep, WeakDep):
            op_name = name_to_buf[dep.name].defining_op_name()
            is_redundant = name_to_dep_count[
                name_to_fused_node[op_name].get_name()
            ] > 0 and node.scheduler.fusable_weak_dep(
                dep, name_to_fused_node[op_name], node
            )
            # These can occur because fused nodes always gather deps from their snodes
            # If B has a weakdep on A
            # B gets fused with C, then any time BC is fused, the weakdep will reappear
            is_self_dep = name_to_fused_node[op_name] == node
            return is_redundant or is_self_dep
        else:
            return False

    deps_to_prune = OrderedSet(
        dep for dep in node.unmet_dependencies if should_prune(dep)
    )

    if deps_to_prune:
        node.unmet_dependencies = node.unmet_dependencies - deps_to_prune
        node.set_read_writes(node.read_writes.remove_reads(deps_to_prune))

