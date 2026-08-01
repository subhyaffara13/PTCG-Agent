
def parseGDEF(lines, font):
    container = ttLib.getTableClass("GDEF")()
    log.debug("Parsing GDEF")
    self = ot.GDEF()
    fields = {
        "class definition begin": (
            "GlyphClassDef",
            lambda lines, font: parseClassDef(lines, font, klass=ot.GlyphClassDef),
        ),
        "attachment list begin": ("AttachList", parseAttachList),
        "carets begin": ("LigCaretList", parseCaretList),
        "mark attachment class definition begin": (
            "MarkAttachClassDef",
            lambda lines, font: parseClassDef(lines, font, klass=ot.MarkAttachClassDef),
        ),
        "markfilter set definition begin": ("MarkGlyphSetsDef", parseMarkFilteringSets),
    }
    for attr, parser in fields.values():
        setattr(self, attr, None)
    while lines.peek() is not None:
        typ = lines.peek()[0].lower()
        if typ not in fields:
            log.debug("Skipping %s", typ)
            next(lines)
            continue
        attr, parser = fields[typ]
        assert getattr(self, attr) is None, attr
        setattr(self, attr, parser(lines, font))
    self.Version = 0x00010000 if self.MarkGlyphSetsDef is None else 0x00010002
    container.table = self
    return container

