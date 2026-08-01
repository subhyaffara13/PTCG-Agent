
def bare_except(logical_line, noqa):
    r"""When catching exceptions, mention specific exceptions when
    possible.

    Okay: except Exception:
    Okay: except BaseException:
    E722: except:
    """
    if noqa:
        return

    match = BLANK_EXCEPT_REGEX.match(logical_line)
    if match:
        yield match.start(), "E722 do not use bare 'except'"

