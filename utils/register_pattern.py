from typing import Callable, Optional, Union

def register_pattern(
	name: str,
	pattern_factory: Union[Callable[[Union[str, bytes]], Pattern], type[Pattern]],
	override: Optional[bool] = None,
) -> None:
	"""
	Registers the specified pattern factory.

	*name* (:class:`str`) is the name to register the pattern factory under.

	*pattern_factory* (:class:`~collections.abc.Callable`) is used to compile
	patterns. It must accept an uncompiled pattern (:class:`str`) and return the
	compiled pattern (:class:`.Pattern`).

	*override* (:class:`bool` or :data:`None`) optionally is whether to allow
	overriding an already registered pattern under the same name (:data:`True`),
	instead of raising an :exc:`.AlreadyRegisteredError` (:data:`False`). Default
	is :data:`None` for :data:`False`.
	"""
	if not isinstance(name, str):
		raise TypeError(f"{name=!r} is not a string.")

	if not callable(pattern_factory):
		raise TypeError(f"{pattern_factory=!r} is not callable.")

	if name in _registered_patterns and not override:
		raise AlreadyRegisteredError(name, _registered_patterns[name])

	_registered_patterns[name] = pattern_factory  # type: ignore


def register_pattern(type_, pattern, router=purl_router):
    """
    Register a pattern with its type.
    """

    def endpoint(url):
        return purl_from_pattern(type_, pattern, url)

    router.append(pattern, endpoint)

