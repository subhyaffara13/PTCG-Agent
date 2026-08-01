
def buildVarDevTable(varIdx):
    self = ot.Device()
    self.DeltaFormat = 0x8000
    self.StartSize = varIdx >> 16
    self.EndSize = varIdx & 0xFFFF
    return self


def buildVarDevTable(store_builder, master_values):
    if allEqual(master_values):
        return master_values[0], None
    base, varIdx = store_builder.storeMasters(master_values)
    return base, builder.buildVarDevTable(varIdx)

