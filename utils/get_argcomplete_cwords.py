import os

def get_argcomplete_cwords() -> t.Optional[t.List[str]]:
    """Get current words prior to completion point

    This is normally done in the `argcomplete.CompletionFinder` constructor,
    but is exposed here to allow `traitlets` to follow dynamic code-paths such
    as determining whether to evaluate a subcommand.
    """
    if "_ARGCOMPLETE" not in os.environ:
        return None

    comp_line = os.environ["COMP_LINE"]
    comp_point = int(os.environ["COMP_POINT"])
    # argcomplete.debug("splitting COMP_LINE for:", comp_line, comp_point)
    comp_words: t.List[str]
    try:
        (
            cword_prequote,
            cword_prefix,
            cword_suffix,
            comp_words,
            last_wordbreak_pos,
        ) = argcomplete.split_line(comp_line, comp_point)  # type:ignore[attr-defined,no-untyped-call]
    except ModuleNotFoundError:
        return None

    # _ARGCOMPLETE is set by the shell script to tell us where comp_words
    # should start, based on what we're completing.
    # 1: <script> [args]
    # 2: python <script> [args]
    # 3: python -m <module> [args]
    start = int(os.environ["_ARGCOMPLETE"]) - 1
    comp_words = comp_words[start:]

    # argcomplete.debug("prequote=", cword_prequote, "prefix=", cword_prefix, "suffix=", cword_suffix, "words=", comp_words, "last=", last_wordbreak_pos)
    return comp_words  # noqa: RET504

