
def desubroutinize(cff):
    for fontName in cff.fontNames:
        font = cff[fontName]
        cs = font.CharStrings
        for c in cs.values():
            desubroutinizeCharString(c)
        # Delete all the local subrs
        if hasattr(font, "FDArray"):
            for fd in font.FDArray:
                pd = fd.Private
                if hasattr(pd, "Subrs"):
                    del pd.Subrs
                if "Subrs" in pd.rawDict:
                    del pd.rawDict["Subrs"]
        else:
            pd = font.Private
            if hasattr(pd, "Subrs"):
                del pd.Subrs
            if "Subrs" in pd.rawDict:
                del pd.rawDict["Subrs"]
    # as well as the global subrs
    cff.GlobalSubrs.clear()


def desubroutinize(self):
    self.cff.desubroutinize()

