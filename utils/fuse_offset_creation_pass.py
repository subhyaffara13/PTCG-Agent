
def fuse_offset_creation_pass(graph: torch.fx.Graph) -> int:
    """
    Here offset node means seed << 32 + offset, will unpacked in lowering.py:inductor_random()
    Horizontally fuse all the seed generation on each device
        a = inductor_prims.rand_eager_offset(offset, dev)
        b = inductor_prims.rand_eager_offset(offset, dev)
    Becomes:
        offsets = inductor_prims.rand_eager_offsets([offset1, offset2...], dev)
        a = torch.ops.aten.select.int(offsets, 0, 0)
        b = torch.ops.aten.select.int(offsets, 0, 1)
    We do this because seed creation is entirely launch overhead bound.
    """
    device_offsets = collections.defaultdict(list)
    for node in graph.nodes:
        if CallFunctionVarArgs(inductor_prims.rand_eager_offset).match(node):
            device_offsets[node.args[1]].append(node)

    if not device_offsets:
        return 0

    for device, offsets in device_offsets.items():
        with graph.inserting_before(offsets[0]):
            offs = [n.args[0] for n in offsets]
            combined = graph.call_function(
                inductor_prims.rand_eager_offsets, (offs, device)
            )
            with V.fake_mode:
                combined.meta["val"] = torch.empty(
                    [len(offsets), 2], device=device, dtype=torch.int64
                )
                combined.meta["tensor_meta"] = _extract_tensor_metadata(
                    combined.meta["val"]
                )

        for idx, offset in enumerate(offsets):
            with graph.inserting_before(offset):
                new_state = graph.call_function(
                    torch.ops.aten.select.int, (combined, 0, idx)
                )
            offset.replace_all_uses_with(new_state)
            new_state.meta.update(offset.meta)
            graph.erase_node(offset)

    return len(device_offsets)

