
def _meet_replace_sigs(sigs: list[CallableType]) -> CallableType:
    """
    Produces the lowest bound of the 'replace' signatures of multiple dataclasses.
    """
    args = {
        name: (typ, kind)
        for name, typ, kind in zip(sigs[0].arg_names, sigs[0].arg_types, sigs[0].arg_kinds)
    }

    for sig in sigs[1:]:
        sig_args = {
            name: (typ, kind)
            for name, typ, kind in zip(sig.arg_names, sig.arg_types, sig.arg_kinds)
        }
        for name in (*args.keys(), *sig_args.keys()):
            sig_typ, sig_kind = args.get(name, (UninhabitedType(), ARG_NAMED_OPT))
            sig2_typ, sig2_kind = sig_args.get(name, (UninhabitedType(), ARG_NAMED_OPT))
            args[name] = (
                meet_types(sig_typ, sig2_typ),
                ARG_NAMED_OPT if sig_kind == sig2_kind == ARG_NAMED_OPT else ARG_NAMED,
            )

    return sigs[0].copy_modified(
        arg_names=list(args.keys()),
        arg_types=[typ for typ, _ in args.values()],
        arg_kinds=[kind for _, kind in args.values()],
    )

