
def set_validation(cls: Type['DataclassT'], value: bool) -> Generator[Type['DataclassT'], None, None]:
    original_run_validation = cls.__pydantic_run_validation__
    try:
        cls.__pydantic_run_validation__ = value
        yield cls
    finally:
        cls.__pydantic_run_validation__ = original_run_validation

