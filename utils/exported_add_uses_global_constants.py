
def ExportedAddUsesGlobalConstants(builder, usesGlobalConstants):
    builder.PrependBoolSlot(16, usesGlobalConstants, 0)

