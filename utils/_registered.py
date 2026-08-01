
def _registered(typ: Type[T]) -> Type[T]:
    pass


def _registered(typ: 'ConstrainedNumberMeta') -> 'ConstrainedNumberMeta':
    pass


def _registered(typ: Union[Type[T], 'ConstrainedNumberMeta']) -> Union[Type[T], 'ConstrainedNumberMeta']:
    # In order to generate valid examples of constrained types, Hypothesis needs
    # to inspect the type object - so we keep a weakref to each contype object
    # until it can be registered.  When (or if) our Hypothesis plugin is loaded,
    # it monkeypatches this function.
    # If Hypothesis is never used, the total effect is to keep a weak reference
    # which has minimal memory usage and doesn't even affect garbage collection.
    _DEFINED_TYPES.add(typ)
    return typ


def _registered(typ: Type[pydantic.types.T]) -> Type[pydantic.types.T]:
    pass


def _registered(typ: pydantic.types.ConstrainedNumberMeta) -> pydantic.types.ConstrainedNumberMeta:
    pass


def _registered(
    typ: Union[Type[pydantic.types.T], pydantic.types.ConstrainedNumberMeta]
) -> Union[Type[pydantic.types.T], pydantic.types.ConstrainedNumberMeta]:
    # This function replaces the version in `pydantic.types`, in order to
    # effect the registration of new constrained types so that Hypothesis
    # can generate valid examples.
    pydantic.types._DEFINED_TYPES.add(typ)
    for supertype, resolver in RESOLVERS.items():
        if issubclass(typ, supertype):
            st.register_type_strategy(typ, resolver(typ))  # type: ignore
            return typ
    raise NotImplementedError(f'Unknown type {typ!r} has no resolver to register')  # pragma: no cover

