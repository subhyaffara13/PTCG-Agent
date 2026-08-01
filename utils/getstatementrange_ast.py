
def getstatementrange_ast(
    lineno: int,
    source: Source,
    assertion: bool = False,
    astnode: ast.AST | None = None,
) -> tuple[ast.AST, int, int]:
    if astnode is None:
        content = str(source)
        # See #4260:
        # Don't produce duplicate warnings when compiling source to find AST.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            astnode = ast.parse(content, "source", "exec")

    start, end = get_statement_startend2(lineno, astnode)
    # We need to correct the end:
    # - ast-parsing strips comments
    # - there might be empty lines
    # - we might have lesser indented code blocks at the end
    if end is None:
        end = len(source.lines)

    if end > start + 1:
        # Make sure we don't span differently indented code blocks
        # by using the BlockFinder helper used which inspect.getsource() uses itself.
        block_finder = inspect.BlockFinder()
        # If we start with an indented line, put blockfinder to "started" mode.
        block_finder.started = (
            bool(source.lines[start]) and source.lines[start][0].isspace()
        )
        it = ((x + "\n") for x in source.lines[start:end])
        try:
            for tok in tokenize.generate_tokens(lambda: next(it)):
                block_finder.tokeneater(*tok)
        except (inspect.EndOfBlock, IndentationError):
            end = block_finder.last + start
        except Exception:
            pass

    # The end might still point to a comment or empty line, correct it.
    end = min(end, len(source.lines))
    while end:
        line = source.lines[end - 1].lstrip()
        if line.startswith("#") or not line:
            end -= 1
        else:
            break
    return astnode, start, end

