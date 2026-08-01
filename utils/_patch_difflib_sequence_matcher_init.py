
def _patch_difflib_sequence_matcher_init():
    """Context patching `difflib.SequenceMatcher` for fx readable graph.

    Under this context, the `autojunk` argument of `difflib.SequenceMatcher` will always
    be considered as `False`. This is to prevent `difflib.SequenceMatcher` recognizing
    stacktrace messages in fx readable graph as junk, as these messages tend to be long (>200)
    and repeat multiple times, which falls under the junk filter criteria.

    `difflib.SequenceMatcher` is used underneath by all sorts of diffing functions
    in `difflib`, including `difflib.unified_diff`, `difflib.ndiff`, `difflib.context_diff`.
    Unfortunately, there is no way to pass `autojunk` argument to these functions, and
    they all default to `True`. This context patching will affect all of them.

    `Reference: Automatic junk heuristic <https://docs.python.org/3/library/difflib.html>`_
    """
    original_init = difflib.SequenceMatcher.__init__

    def patched_init(self, isjunk=None, a="", b="", autojunk=True) -> None:
        original_init(self, isjunk, a, b, autojunk=False)

    difflib.SequenceMatcher.__init__ = patched_init  # type: ignore[assignment]
    try:
        yield
    finally:
        difflib.SequenceMatcher.__init__ = original_init  # type: ignore[assignment]

