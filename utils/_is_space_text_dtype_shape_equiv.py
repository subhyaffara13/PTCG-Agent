
def _is_space_text_dtype_shape_equiv(space_1: Text, space_2):
    return (
        isinstance(space_2, Text)
        and space_1.max_length == space_2.max_length
        and space_1.character_set == space_2.character_set
    )

