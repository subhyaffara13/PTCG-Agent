
def desubroutinizeCharString(cs):
    """Desubroutinize a charstring in-place."""
    cs.decompile()
    subrs = getattr(cs.private, "Subrs", [])
    decompiler = _DesubroutinizingT2Decompiler(subrs, cs.globalSubrs, cs.private)
    decompiler.execute(cs)
    cs.program = cs._desubroutinized
    del cs._desubroutinized

