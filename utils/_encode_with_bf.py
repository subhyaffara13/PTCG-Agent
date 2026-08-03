from typing import Dict, Set, Tuple

def _encodeWithBf(valueSet: Set[int], branchFactor: int, height: int) -> bytes:
    if height == 0:
        return _encodeHeader(branchFactor, 0)

    # Build layers bottom-up: layer 0 = leaves (individual values),
    # each higher layer groups bf children into one parent bitmask.
    layers: list[Dict[int, int]] = [{}]  # list of dicts: nodeIndex -> bitmask

    for v in valueSet:
        nodeIndex = v // branchFactor
        bitPos = v % branchFactor
        if nodeIndex not in layers[0]:
            layers[0][nodeIndex] = 0
        layers[0][nodeIndex] |= 1 << bitPos

    for _ in range(1, height):
        prevLayer = layers[-1]
        newLayer: Dict[int, int] = {}
        for nodeIndex, bitmask in prevLayer.items():
            parentIndex = nodeIndex // branchFactor
            bitPos = nodeIndex % branchFactor
            if parentIndex not in newLayer:
                newLayer[parentIndex] = 0
            newLayer[parentIndex] |= 1 << bitPos
        layers.append(newLayer)

    # For zero-node optimization: track count of values in sorted list.
    valuesSorted = sorted(valueSet)

    def rangeCount(lo: int, hi: int) -> int:
        return bisect.bisect_right(valuesSorted, hi) - bisect.bisect_left(
            valuesSorted, lo
        )

    # Emit nodes BFS order (root to leaves).
    # Queue entries: (nodeIndex, depthFromRoot, rangeStart, rangeEnd)
    stream = _OutputBitStream(branchFactor)
    subtreeSize = branchFactor**height
    queue: deque[Tuple[int, int, int, int]] = deque([(0, 0, 0, subtreeSize - 1)])

    while queue:
        nodeIndex, depth, rangeStart, rangeEnd = queue.popleft()
        layerIdx = height - 1 - depth  # layers[0]=leaves, layers[height-1]=root

        bitmask = (
            layers[layerIdx].get(nodeIndex, 0) if 0 <= layerIdx < len(layers) else 0
        )

        # Zero-node optimization: if entire range is filled on an INTERNAL node,
        # write 0 and skip children.  At leaf level we always write the explicit
        # bitmask so the encoding matches the reference.
        if (
            depth < height - 1
            and rangeCount(rangeStart, rangeEnd) == rangeEnd - rangeStart + 1
        ):
            stream.write(0)
            continue

        stream.write(bitmask)

        if bitmask != 0 and depth < height - 1:
            childSize = (rangeEnd - rangeStart + 1) // branchFactor
            bits = bitmask
            while bits:
                bitIndex = _trailingZeros(bits, 32)
                childIndex = nodeIndex * branchFactor + bitIndex
                childStart = rangeStart + bitIndex * childSize
                childEnd = childStart + childSize - 1
                queue.append((childIndex, depth + 1, childStart, childEnd))
                bits &= ~(1 << bitIndex)

    return _encodeHeader(branchFactor, height) + stream.toBytes()

