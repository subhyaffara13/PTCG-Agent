
def _get_combined_plan(
    mgrs: list[BlockManager],
) -> Generator[tuple[BlockPlacement, list[JoinUnit]]]:
    max_len = mgrs[0].shape[0]

    blknos_list = [mgr.blknos for mgr in mgrs]
    pairs = libinternals.get_concat_blkno_indexers(blknos_list)
    for blknos, bp in pairs:
        # assert bp.is_slice_like
        # assert len(bp) > 0

        units_for_bp = []
        for k, mgr in enumerate(mgrs):
            blkno = blknos[k]

            nb = _get_block_for_concat_plan(mgr, bp, blkno, max_len=max_len)
            unit = JoinUnit(nb)
            units_for_bp.append(unit)

        yield bp, units_for_bp

