from typing import Any

def add_request_id(obj: BaseModel, request_id: str | None) -> None:
    obj._request_id = request_id

    # in Pydantic v1, using setattr like we do above causes the attribute
    # to be included when serializing the model which we don't want in this
    # case so we need to explicitly exclude it
    if PYDANTIC_V1:
        try:
            exclude_fields = obj.__exclude_fields__  # type: ignore
        except AttributeError:
            cast(Any, obj).__exclude_fields__ = {"_request_id", "__exclude_fields__"}
        else:
            cast(Any, obj).__exclude_fields__ = {*(exclude_fields or {}), "_request_id", "__exclude_fields__"}

