
def CreateEdgeEnd(builder, nodeIndex, srcArgIndex, dstArgIndex):
    builder.Prep(4, 12)
    builder.PrependInt32(dstArgIndex)
    builder.PrependInt32(srcArgIndex)
    builder.PrependUint32(nodeIndex)
    return builder.Offset()

