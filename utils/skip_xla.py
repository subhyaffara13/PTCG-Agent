
def skipXLA(fn):
    return skipXLAIf(True, "Marked as skipped for XLA")(fn)

