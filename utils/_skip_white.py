
def _skipWhite(data: str, pos: int) -> int:
    m = _whiteRE.match(data, pos)
    newPos = m.regs[0][1]
    assert newPos >= pos
    return newPos

