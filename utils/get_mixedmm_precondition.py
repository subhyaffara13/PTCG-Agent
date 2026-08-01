
def get_mixedmm_precondition(metadata: AHMetadata, context: AHContext) -> bool:
    m = context.get_value("m")
    k = context.get_value("k")
    n = context.get_value("n")
    if m > 128 or k < 1024 or n < 1024:
        return False
    mat1_iscontig = context.get_value("mat1_iscontig")
    mat2_iscontig = context.get_value("mat2_iscontig")
    return mat1_iscontig and not mat2_iscontig

