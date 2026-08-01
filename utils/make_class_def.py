
def makeClassDef(classDefs, font, klass=ot.Coverage):
    if not classDefs:
        return None
    self = klass()
    self.classDefs = dict(classDefs)
    return self

