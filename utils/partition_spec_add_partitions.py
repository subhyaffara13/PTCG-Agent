
def PartitionSpecAddPartitions(builder, partitions):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(partitions), 0)

