
def _SinglePosUpgradeToFormat2(self):
    if self.Format == 2:
        return self

    ret = ot.SinglePos()
    ret.Format = 2
    ret.Coverage = self.Coverage
    ret.ValueFormat = self.ValueFormat
    ret.Value = [self.Value for _ in ret.Coverage.glyphs]
    ret.ValueCount = len(ret.Value)

    return ret

