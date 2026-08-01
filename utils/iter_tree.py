
def iter_tree(root, on_error=None, follow_links=None):
	"""
	.. version-deprecated:: 0.10.0
		This is an alias for the :func:`.iter_tree_files` function.
	"""
	return iter_tree_files(root, on_error=on_error, follow_links=follow_links)

