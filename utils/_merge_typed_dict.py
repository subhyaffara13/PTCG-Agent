
def _merge_typed_dict(preprocessor_typed_dict: type, modality_typed_dict: type) -> type:
    return TypedDict(
        "merged_typed_dict",
        {**preprocessor_typed_dict.__annotations__, **modality_typed_dict.__annotations__},
        total=False,
    )

