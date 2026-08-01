
def reverse_aliases(app: Application) -> dict[str, list[str]]:
    """Produce a mapping of trait names to lists of command line aliases."""
    res = defaultdict(list)
    for alias, trait in app.aliases.items():
        res[trait].append(alias)

    # Flags also often act as aliases for a boolean trait.
    # Treat flags which set one trait to True as aliases.
    for flag, (cfg, _) in app.flags.items():
        if len(cfg) == 1:
            classname = next(iter(cfg))
            cls_cfg = cfg[classname]
            if len(cls_cfg) == 1:
                traitname = next(iter(cls_cfg))
                if cls_cfg[traitname] is True:
                    res[classname + "." + traitname].append(flag)

    return res

