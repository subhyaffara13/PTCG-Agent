
def writesimple(tag, self, writer, *attrkeys):
    attrs = dict([(k, getattr(self, k)) for k in attrkeys])
    writer.simpletag(tag, **attrs)
    writer.newline()

