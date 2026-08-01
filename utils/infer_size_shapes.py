
def infer_size_shapes(a: ShapeType, b: ShapeType) -> tuple[int, ...]:
    ndim = max(len(a), len(b))
    expandedSizes = [0] * ndim

    for i in range(ndim - 1, -1, -1):
        offset = ndim - 1 - i
        dimA = len(a) - 1 - offset
        dimB = len(b) - 1 - offset
        sizeA = a[dimA] if dimA >= 0 else 1
        sizeB = b[dimB] if dimB >= 0 else 1

        torch._check(
            (sizeA == sizeB) or (sizeA == 1) or (sizeB == 1),
            lambda: (
                f"The size of tensor a ({sizeA}) must match the size of "
                f"tensor b ({sizeB}) at non-jagged dimension {i}"
            ),
        )

        # 1s map to the other size (even 0)
        expandedSizes[i] = sizeB if sizeA == 1 else sizeA

    return tuple(expandedSizes)

