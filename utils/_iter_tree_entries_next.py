import os
from typing import Callable, Optional

def _iter_tree_entries_next(
	root_full: str,
	dir_rel: str,
	memo: dict[str, str],
	on_error: Optional[Callable[[OSError], None]],
	follow_links: bool,
) -> Iterator['TreeEntry']:
	"""
	Scan the directory for all descendant files.

	*root_full* (:class:`str`) the absolute path to the root directory.

	*dir_rel* (:class:`str`) the path to the directory to scan relative to
	*root_full*.

	*memo* (:class:`dict`) keeps track of ancestor directories encountered. Maps
	each ancestor real path (:class:`str`) to relative path (:class:`str`).

	*on_error* (:class:`~collections.abc.Callable` or :data:`None`) optionally is
	the error handler for file-system exceptions.

	*follow_links* (:class:`bool`) is whether to walk symbolic links that resolve
	to directories.

	Yields each entry (:class:`.TreeEntry`).
	"""
	dir_full = os.path.join(root_full, dir_rel)
	dir_real = os.path.realpath(dir_full)

	# Remember each encountered ancestor directory and its canonical (real) path.
	# If a canonical path is encountered more than once, recursion has occurred.
	if dir_real not in memo:
		memo[dir_real] = dir_rel
	else:
		raise RecursionError(real_path=dir_real, first_path=memo[dir_real], second_path=dir_rel)

	with os.scandir(dir_full) as scan_iter:
		node_ent: os.DirEntry
		for node_ent in scan_iter:
			node_rel = os.path.join(dir_rel, node_ent.name)

			# Inspect child node.
			try:
				node_lstat = node_ent.stat(follow_symlinks=False)
			except OSError as e:
				if on_error is not None:
					on_error(e)
				continue

			if node_ent.is_symlink():
				# Child node is a link, inspect the target node.
				try:
					node_stat = node_ent.stat()
				except OSError as e:
					if on_error is not None:
						on_error(e)
					continue
			else:
				node_stat = node_lstat

			if node_ent.is_dir(follow_symlinks=follow_links):
				# Child node is a directory, recurse into it and yield its descendant
				# files.
				yield TreeEntry(node_ent.name, node_rel, node_lstat, node_stat)

				yield from _iter_tree_entries_next(root_full, node_rel, memo, on_error, follow_links)

			elif node_ent.is_file() or node_ent.is_symlink():
				# Child node is either a file or an unfollowed link, yield it.
				yield TreeEntry(node_ent.name, node_rel, node_lstat, node_stat)

	# NOTE: Make sure to remove the canonical (real) path of the directory from
	# the ancestors memo once we are done with it. This allows the same directory
	# to appear multiple times. If this is not done, the second occurrence of the
	# directory will be incorrectly interpreted as a recursion. See
	# <https://github.com/cpburnz/python-path-specification/pull/7>.
	del memo[dir_real]

