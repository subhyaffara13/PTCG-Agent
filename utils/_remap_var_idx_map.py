
def _remapVarIdxMap(table, attrName, varIndexMapping, glyphOrder):
    oldMapping = getattr(table, attrName).mapping
    newMapping = [varIndexMapping[oldMapping[glyphName]] for glyphName in glyphOrder]
    setattr(table, attrName, builder.buildVarIdxMap(newMapping, glyphOrder))

