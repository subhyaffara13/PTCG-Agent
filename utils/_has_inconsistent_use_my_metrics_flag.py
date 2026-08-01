
def _has_inconsistent_use_my_metrics_flag(
    master_glyf, glyph_name, flagged_components, expected_num_components
) -> bool:
    master_glyph = master_glyf.get(glyph_name)
    # 'sparse' glyph master doesn't contribute. Besides when components don't match
    # the VF build is going to fail anyway, so be lenient here.
    if (
        master_glyph is not None
        and master_glyph.isComposite()
        and len(master_glyph.components) == expected_num_components
    ):
        for i, base_glyph in flagged_components:
            comp = master_glyph.components[i]
            if comp.glyphName != base_glyph:
                break
            if not (comp.flags & USE_MY_METRICS):
                return True
    return False

