
def is_model_class(cls: Any) -> TypeGuard[type[BaseModel]]:
    """Returns true if cls is a _proper_ subclass of BaseModel, and provides proper type-checking,
    unlike raw calls to lenient_issubclass.
    """
    BaseModel = import_cached_base_model()

    return lenient_issubclass(cls, BaseModel) and cls is not BaseModel

