
def validate_symbols(symbols, validate_keys=False):
    """
    Return a tuple of (`warnings`, `errors`) given a sequence of ``symbols``
    LicenseSymbol-like objects.

    - `warnings` is a list of validation warnings messages (possibly empty if
      there were no warnings).
    - `errors` is a list of validation error messages (possibly empty if there
      were no errors).

    Keys and aliases are cleaned and validated for uniqueness.

    If ``validate_keys`` also validate that license keys are known keys.
    """

    # collection used for checking unicity and correctness
    seen_keys = set()
    seen_aliases = {}
    seen_exceptions = set()

    # collections to accumulate invalid data and build error messages at the end
    not_symbol_classes = []
    dupe_keys = set()
    dupe_exceptions = set()
    dupe_aliases = defaultdict(list)
    invalid_keys_as_kw = set()
    invalid_alias_as_kw = defaultdict(list)

    # warning
    warning_dupe_aliases = set()

    for symbol in symbols:
        if not isinstance(symbol, LicenseSymbol):
            not_symbol_classes.append(symbol)
            continue

        key = symbol.key
        key = key.strip()
        keyl = key.lower()

        # ensure keys are unique
        if keyl in seen_keys:
            dupe_keys.add(key)

        # key cannot be an expression keyword
        if keyl in KEYWORDS_STRINGS:
            invalid_keys_as_kw.add(key)

        # keep a set of unique seen keys
        seen_keys.add(keyl)

        # aliases is an optional attribute
        aliases = getattr(symbol, "aliases", [])
        initial_alias_len = len(aliases)

        # always normalize aliases for spaces and case
        aliases = set([" ".join(alias.lower().strip().split()) for alias in aliases])

        # KEEP UNIQUES, remove empties
        aliases = set(a for a in aliases if a)

        # issue a warning when there are duplicated or empty aliases
        if len(aliases) != initial_alias_len:
            warning_dupe_aliases.add(key)

        # always add a lowercase key as an alias
        aliases.add(keyl)

        for alias in aliases:
            # note that we do not treat as an error the presence of a duplicated
            # alias pointing to the same key

            # ensure that a possibly duplicated alias does not point to another key
            aliased_key = seen_aliases.get(alias)
            if aliased_key and aliased_key != keyl:
                dupe_aliases[alias].append(key)

            # an alias cannot be an expression keyword
            if alias in KEYWORDS_STRINGS:
                invalid_alias_as_kw[key].append(alias)

            seen_aliases[alias] = keyl

        if symbol.is_exception:
            if keyl in seen_exceptions:
                dupe_exceptions.add(keyl)
            else:
                seen_exceptions.add(keyl)

    # build warning and error messages from invalid data
    errors = []
    for ind in sorted(not_symbol_classes):
        errors.append(f"Invalid item: not a LicenseSymbol object: {ind!r}.")

    for dupe in sorted(dupe_keys):
        errors.append(f"Invalid duplicated license key: {dupe!r}.")

    for dalias, dkeys in sorted(dupe_aliases.items()):
        dkeys = ", ".join(dkeys)
        errors.append(
            f"Invalid duplicated alias pointing to multiple keys: "
            f"{dalias} point to keys: {dkeys!r}."
        )

    for ikey, ialiases in sorted(invalid_alias_as_kw.items()):
        ialiases = ", ".join(ialiases)
        errors.append(
            f"Invalid aliases: an alias cannot be an expression keyword. "
            f"key: {ikey!r}, aliases: {ialiases}."
        )

    for dupe in sorted(dupe_exceptions):
        errors.append(f"Invalid duplicated license exception key: {dupe}.")

    for ikw in sorted(invalid_keys_as_kw):
        errors.append(f"Invalid key: a key cannot be an expression keyword: {ikw}.")

    warnings = []
    for dupe_alias in sorted(dupe_aliases):
        errors.append(f"Duplicated or empty aliases ignored for license key: {dupe_alias!r}.")

    return warnings, errors

