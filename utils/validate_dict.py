
def validate_dict(data: dict, model) -> dict:
    return model(**data).model_dump(by_alias=True, exclude_unset=True)


def validate_dict(data: dict, model) -> dict:
    return model(**data).model_dump(exclude_unset=True, by_alias=True)

