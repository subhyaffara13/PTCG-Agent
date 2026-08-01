
def DisabledSafetyCheckAddKind(builder, kind):
    builder.PrependInt8Slot(0, kind, 0)

