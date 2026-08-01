
def make_gitignore_backend(
	name: BackendNamesHint,
	patterns: Sequence[Pattern],
) -> _Backend:
	"""
	Create the specified backend with the supplied patterns for
	:class:`~pathspec.gitignore.GitIgnoreSpec`.

	*name* (:class:`str`) is the name of the backend.

	*patterns* (:class:`.Iterable` of :class:`.Pattern`) contains the compiled
	patterns.

	Returns the backend (:class:`._Backend`).
	"""
	if name == 'best':
		name = _BEST_BACKEND

	if name == 'hyperscan':
		return HyperscanGiBackend(cast(Sequence[RegexPattern], patterns))
	elif name == 're2':
		return Re2GiBackend(cast(Sequence[RegexPattern], patterns))
	elif name == 'simple':
		return SimpleGiBackend(cast(Sequence[RegexPattern], patterns))
	else:
		raise ValueError(f"Backend {name=!r} is invalid.")

