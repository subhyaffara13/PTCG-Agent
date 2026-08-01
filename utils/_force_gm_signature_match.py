
def _force_gm_signature_match(ep_guards_code: list[str], signature):
    """
    The signature of the originally exported module may not match
    the signature of the unlifted graph module extracted from the
    exported program. The guards code extracted from the exported
    program is based on the former, but the generated guards fn is
    based on the latter; thus we need to reconcile any such diff.
    """

    import re

    # Handle case where signatures may differ in var args.
    orig_arg_names = set()
    for g in ep_guards_code:
        # match substrings of the form L['<name>'][<number>]
        orig_arg_names.update(re.findall(r"L\[\'([^\']+)\'\]\[([0-9]+)\]", g))

    sig_arg_names = set()
    for n in signature.parameters:
        # match substrings of the form <name>_<number>
        sig_arg_names.update(re.findall(r"(.+)_([0-9]+)", n))

    # replace L['<name>'][<number>] with L['<name>_<number>']
    new_guards_code = ep_guards_code
    for match in orig_arg_names:
        if match in sig_arg_names:
            base, idx = match
            new_guards_code = [
                g.replace(f"L['{base}'][{idx}]", f"L['{base}_{idx}']")
                for g in new_guards_code
            ]

    return new_guards_code

