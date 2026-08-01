
def meta_embedding_bag_forward_only(weight, indices, offsets, *args):
    output, offset2bag, bag_size, max_indices = meta_embedding_bag(
        weight, indices, offsets, *args
    )
    if device_hint(offsets) == "cpu":
        bag_size = offsets.new_empty(offsets.size())
    return output, offset2bag, bag_size, max_indices

