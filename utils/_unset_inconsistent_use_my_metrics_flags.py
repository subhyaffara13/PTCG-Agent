
def _unset_inconsistent_use_my_metrics_flags(vf, master_fonts):
    """Clear USE_MY_METRICS on composite components if inconsistent across masters.

    If a composite glyph's component has USE_MY_METRICS set differently among
    the masters, the flag is removed from the variable font's glyf table so that
    advance widths are not determined by that single component's phantom points.
    """
    glyf = vf["glyf"]
    master_glyfs = [m["glyf"] for m in master_fonts if "glyf" in m]
    if not master_glyfs:
        # Should not happen: at least the base master (as copied into vf) has glyf
        return

    for glyph_name in glyf.keys():
        glyph = glyf[glyph_name]
        if not glyph.isComposite():
            continue

        # collect indices of component(s) that carry the USE_MY_METRICS flag.
        # This is supposed to be 1 component per composite, but you never know.
        flagged_components = [
            (i, comp.glyphName)
            for i, comp in enumerate(glyph.components)
            if (comp.flags & USE_MY_METRICS)
        ]
        if not flagged_components:
            # Nothing to fix
            continue

        # Verify that for all master glyf tables that contribute this glyph, the
        # corresponding component (same glyphName and index) also carries USE_MY_METRICS
        # and unset the flag if not.
        expected_num_components = len(glyph.components)
        if any(
            _has_inconsistent_use_my_metrics_flag(
                master_glyf, glyph_name, flagged_components, expected_num_components
            )
            for master_glyf in master_glyfs
        ):
            comp_names = [name for _, name in flagged_components]
            log.info(
                "Composite glyph '%s' has inconsistent USE_MY_METRICS flags across "
                "masters; clearing the flag on component%s %s",
                glyph_name,
                "s" if len(comp_names) > 1 else "",
                comp_names if len(comp_names) > 1 else comp_names[0],
            )
            for i, _ in flagged_components:
                glyph.components[i].flags &= ~USE_MY_METRICS

