
def make_pathspec_backend(
	name: BackendNamesHint,
	patterns: Sequence[Pattern],
) -> _Backend:
	"""
	Create the specified backend with the supplied patterns for
	:class:`~pathspec.pathspec.PathSpec`.

	*name* (:class:`str`) is the name of the backend.

	*patterns* (:class:`Iterable` of :class:`Pattern`) contains the compiled
	patterns.

	Returns the backend (:class:`._Backend`).
	"""
	if name == 'best':
		name = _BEST_BACKEND

	if name == 'hyperscan':
		return HyperscanPsBackend(cast(Sequence[RegexPattern], patterns))
	elif name == 're2':
		return Re2PsBackend(cast(Sequence[RegexPattern], patterns))
	elif name == 'simple':
		return SimplePsBackend(patterns)
	else:
		raise ValueError(f"Backend {name=!r} is invalid.")

