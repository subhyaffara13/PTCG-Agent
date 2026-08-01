
def segmented_accessor(elements, raw_segments, idx):
    """
    Returns a slice of elements corresponding to the idx-th segment.

      elements: a sliceable container (operands or results).
      raw_segments: an mlir.ir.Attribute, of DenseI32Array subclass containing
          sizes of the segments.
      idx: index of the segment.
    """
    segments = _cext.ir.DenseI32ArrayAttr(raw_segments)
    start = sum(segments[i] for i in range(idx))
    end = start + segments[idx]
    return elements[start:end]

