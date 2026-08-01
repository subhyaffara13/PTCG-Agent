
def parseLookup(lines, tableTag, font, lookupMap=None):
    line = lines.expect("lookup")
    _, name, typ = line
    log.debug("Parsing lookup type %s %s", typ, name)
    lookup = ot.Lookup()
    lookup.LookupFlag, filterset = parseLookupFlags(lines)
    if filterset is not None:
        lookup.MarkFilteringSet = filterset
    lookup.LookupType, parseLookupSubTable = {
        "GSUB": {
            "single": (1, parseSingleSubst),
            "multiple": (2, parseMultiple),
            "alternate": (3, parseAlternate),
            "ligature": (4, parseLigature),
            "context": (5, parseContextSubst),
            "chained": (6, parseChainedSubst),
            "reversechained": (8, parseReverseChainedSubst),
        },
        "GPOS": {
            "single": (1, parseSinglePos),
            "pair": (2, parsePair),
            "kernset": (2, parseKernset),
            "cursive": (3, parseCursive),
            "mark to base": (4, parseMarkToBase),
            "mark to ligature": (5, parseMarkToLigature),
            "mark to mark": (6, parseMarkToMark),
            "context": (7, parseContextPos),
            "chained": (8, parseChainedPos),
        },
    }[tableTag][typ]

    with lines.until("lookup end"):
        subtables = []

        while lines.peek():
            with lines.until(("% subtable", "subtable end")):
                while lines.peek():
                    subtable = parseLookupSubTable(lines, font, lookupMap)
                    assert lookup.LookupType == subtable.LookupType
                    subtables.append(subtable)
            if lines.peeks()[0] in ("% subtable", "subtable end"):
                next(lines)
    lines.expect("lookup end")

    lookup.SubTable = subtables
    lookup.SubTableCount = len(lookup.SubTable)
    if lookup.SubTableCount == 0:
        # Remove this return when following is fixed:
        # https://github.com/fonttools/fonttools/issues/789
        return None
    return lookup

