from typing import Set, Tuple

def _decodeImpl(
    data: bytes, branchFactor: int, height: int, bias: int, maxValue: int
) -> Tuple[Set[int], int]:
    if height == 0:
        # 1 byte was used for the header.
        return (set(), 1)

    bitStream = _InputBitStream(data, branchFactor)
    result: Set[int] = set()
    # Queue entries are (startValue, depth), where startValue is the first
    # integer that could be covered by this node.
    queue: deque[Tuple[int, int]] = deque()
    queue.append((0, 1))

    while queue:
        start, depth = queue.popleft()
        bits = bitStream.next()
        if bits is None:
            raise SparseBitSetDecodeError("Unexpected end of data")

        # all bits were were zero which is a special command to completely fill
        # in all integers covered by this node.
        if bits == 0:
            exp = height - depth + 1
            nodeSize = branchFactor**exp
            fillStart = start + bias
            if fillStart > maxValue:
                continue
            fillEnd = min(maxValue, start + nodeSize - 1 + bias)
            if fillStart < 0:
                fillStart = 0
            if fillStart <= fillEnd:
                result.update(range(fillStart, fillEnd + 1))
            continue

        # Non-zero node: each set bit identifies a child/value.
        exp = height - depth
        nextNodeSize = branchFactor**exp
        while True:
            bitIndex = _trailingZeros(bits, 32)
            if bitIndex == 32:
                break
            if depth == height:
                val = start + bitIndex + bias
                if val > maxValue:
                    queue.clear()
                    break
                if val >= 0:
                    result.add(val)
            else:
                startDelta = bitIndex * nextNodeSize
                queue.append((start + startDelta, depth + 1))
            bits &= ~(1 << bitIndex)

    return (result, bitStream.bytesConsumed())

