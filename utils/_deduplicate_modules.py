
def _deduplicate_modules(partitions):
    redirected_call_indices = {}
    for shared_submodules in partitions:
        for i, entry in enumerate(shared_submodules):
            child_fqn = _call_name(entry.fqn, entry.call_idx)
            target = _compute_accessor(entry.parent_fqn, child_fqn)
            deduplicated = False
            # Iterate over all previously seen modules, and deduplicate if possible
            for seen in shared_submodules[:i]:
                if _check_graph_equivalence(seen.module, entry.module):
                    parent = entry.parent_module
                    # Since graphs are equivalent, we can deduplicate.
                    # There are two cases.
                    if seen.fqn == entry.fqn:
                        # Case 1: The current module has the same fqn as the seen module.
                        # In this case we have generated a call name that can be optimized away.
                        # So we remove the current module from the hierarchy and replace
                        # the current call name with the seen call name in the parent graph.
                        *prefix, name = target.split(".")
                        _get_attr_via_attr_list(parent, prefix)._modules.pop(name)
                        seen_child_fqn = _call_name(seen.fqn, seen.call_idx)
                        seen_target = _compute_accessor(
                            entry.parent_fqn, seen_child_fqn
                        )
                        entry.parent_call_module.target = seen_target
                        redirected_call_indices[child_fqn] = seen_child_fqn
                        break
                    elif not deduplicated:
                        # Case 2: The current module has a different fqn than the seen module.
                        # In this case we replace the current module with the seen module.
                        # There should be nothing pointing to the current module any more,
                        # so it can be garbage collected.
                        # NOTE: We *do not* replace the current call name with the seen call name
                        # in the parent graph, because this will lose information on which fqn
                        # was actually called. However, it is possible that the current call name
                        # will be optimized away when we find another seen module with the same fqn,
                        # so we do not break out of the loop yet.
                        parent.set_submodule(target, seen.module)
                        deduplicated = True

    return redirected_call_indices

