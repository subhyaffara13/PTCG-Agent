
def supports_vec_to_sequence(vec_type: RVec) -> bool:
    return vec_api_by_item_type.get(vec_type.item_type) is not None or vec_type.depth() == 0

