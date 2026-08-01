
def parseCmap(lines, font):
    container = ttLib.getTableClass("cmap")()
    log.debug("Parsing cmap")
    tables = []
    while lines.peek() is not None:
        lines.expect("cmap subtable %d" % len(tables))
        platId, encId, fmt, lang = [
            parseCmapId(lines, field)
            for field in ("platformID", "encodingID", "format", "language")
        ]
        table = cmap_classes[fmt](fmt)
        table.platformID = platId
        table.platEncID = encId
        table.language = lang
        table.cmap = {}
        line = next(lines)
        while line[0] != "end subtable":
            table.cmap[int(line[0], 16)] = line[1]
            line = next(lines)
        tables.append(table)
    container.tableVersion = 0
    container.tables = tables
    return container

