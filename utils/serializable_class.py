from typing import Callable, Optional, Union

def serializable_class(
    cls: Literal[None] = None, *,
    name: Optional[str] = ...,
    serialization_types: Optional[Iterable[SerializationType]] = ...,
    ignore_during_deserialization: Optional[Iterable[str]] = ...,
    ignore_unknown_during_deserialization: bool = ...
) -> Callable[[Type[_T]], Intersection[Type[_T], Type[_JsonSerializable], Type[_XmlSerializable]]]:
    ...


def serializable_class(  # type:ignore[misc] # mypy on py37
    cls: Type[_T], *,
    name: Optional[str] = ...,
    serialization_types: Optional[Iterable[SerializationType]] = ...,
    ignore_during_deserialization: Optional[Iterable[str]] = ...,
    ignore_unknown_during_deserialization: bool = ...
) -> Intersection[Type[_T], Type[_JsonSerializable], Type[_XmlSerializable]]:
    ...


def serializable_class(
    cls: Optional[Type[_T]] = None, *,
    name: Optional[str] = None,
    serialization_types: Optional[Iterable[SerializationType]] = None,
    ignore_during_deserialization: Optional[Iterable[str]] = None,
    ignore_unknown_during_deserialization: bool = False
) -> Union[
    Callable[[Type[_T]], Intersection[Type[_T], Type[_JsonSerializable], Type[_XmlSerializable]]],
    Intersection[Type[_T], Type[_JsonSerializable], Type[_XmlSerializable]]
]:
    """
    Decorator used to tell ``py_serializable`` that a class is to be included in (de-)serialization.

    :param cls: Class
    :param name: Alternative name to use for this Class
    :param serialization_types: Serialization Types that are to be supported for this class.
    :param ignore_during_deserialization: List of properties/elements to ignore during deserialization
    :param ignore_unknown_during_deserialization: Whether to ignore all properties/elements/attributes that are unknown
           to the class during deserialization
    :return:
    """
    # param ignore_unknown_during_deserialization defaults to False, since we deserialize from JSON/XML
    # and both have mechanisms for arbitrary content that might be intended to pass to the constructors:
    # - JSON has `additionalProperties:true`
    # - XML has `##any` and `##other`
    if serialization_types is None:
        serialization_types = _DEFAULT_SERIALIZATION_TYPES

    def decorate(kls: Type[_T]) -> Intersection[Type[_T], Type[_JsonSerializable], Type[_XmlSerializable]]:
        ObjectMetadataLibrary.register_klass(
            klass=kls, custom_name=name, serialization_types=serialization_types or [],
            ignore_during_deserialization=ignore_during_deserialization,
            ignore_unknown_during_deserialization=ignore_unknown_during_deserialization
        )
        return kls

    # See if we're being called as @register_klass or @register_klass().
    if cls is None:
        # We're called with parens.
        return decorate

    # We're called as @register_klass without parens.
    return decorate(cls)

