
def make_hash_func(cls: type[BaseModel]) -> Any:
    getter = operator.itemgetter(*cls.__pydantic_fields__.keys()) if cls.__pydantic_fields__ else lambda _: 0

    def hash_func(self: Any) -> int:
        try:
            return hash(getter(self.__dict__))
        except KeyError:
            # In rare cases (such as when using the deprecated copy method), the __dict__ may not contain
            # all model fields, which is how we can get here.
            # getter(self.__dict__) is much faster than any 'safe' method that accounts for missing keys,
            # and wrapping it in a `try` doesn't slow things down much in the common case.
            return hash(getter(SafeGetItemProxy(self.__dict__)))

    return hash_func

