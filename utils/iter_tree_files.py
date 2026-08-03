import os
from typing import Callable, Optional

def iter_tree_files(
	root: StrPath,
	on_error: Optional[Callable[[OSError], None]] = None,
	follow_links: Optional[bool] = None,
) -> Iterator[str]:
	"""
	Walks the specified directory for all files.

	*root* (:class:`str` or :class:`os.PathLike`) is the root directory to search
	for files.

	*on_error* (:class:`~collections.abc.Callable` or :data:`None`) optionally is
	the error handler for file-system exceptions. It will be called with the
	exception (:exc:`OSError`). Reraise the exception to abort the walk. Default
	is :data:`None` to ignore file-system exceptions.

	*follow_links* (:class:`bool` or :data:`None`) optionally is whether to walk
	symbolic links that resolve to directories. Default is :data:`None` for
	:data:`True`.

	Raises :exc:`.RecursionError` if recursion is detected.

	Returns an :class:`~collections.abc.Iterator` yielding the path to each file
	(:class:`str`) relative to *root*.
	"""
	if on_error is not None and not callable(on_error):
		raise TypeError(f"on_error:{on_error!r} is not callable.")

	if follow_links is None:
		follow_links = True

	yield from _iter_tree_files_next(os.path.abspath(root), '', {}, on_error, follow_links)

