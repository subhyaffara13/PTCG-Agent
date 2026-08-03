from typing import Callable, Union

def resolves(
    typ: Union[type, pydantic.types.ConstrainedNumberMeta]
) -> Callable[[Callable[..., st.SearchStrategy]], Callable[..., st.SearchStrategy]]:  # type: ignore[type-arg]
    def inner(f):  # type: ignore
        assert f not in RESOLVERS
        RESOLVERS[typ] = f
        return f

    return inner

