import re
from typing import Union

def oneOf(validator, oneOf, instance, schema):
    subschemas = enumerate(oneOf)
    all_errors = []
    for index, subschema in subschemas:
        errs = list(validator.descend(instance, subschema, schema_path=index))
        if not errs:
            first_valid = subschema
            break
        all_errors.extend(errs)
    else:
        yield ValidationError(
            f"{instance!r} is not valid under any of the given schemas",
            context=all_errors,
        )

    more_valid = [
        each for _, each in subschemas
        if validator.evolve(schema=each).is_valid(instance)
    ]
    if more_valid:
        more_valid.append(first_valid)
        reprs = ", ".join(repr(schema) for schema in more_valid)
        yield ValidationError(f"{instance!r} is valid under each of {reprs}")


def one_of(
    strs: Union[typing.Iterable[str], str],
    caseless: bool = False,
    use_regex: bool = True,
    as_keyword: bool = False,
    **kwargs,
) -> ParserElement:
    """Helper to quickly define a set of alternative :class:`Literal` s,
    and makes sure to do longest-first testing when there is a conflict,
    regardless of the input order, but returns
    a :class:`MatchFirst` for best performance.

    :param strs: a string of space-delimited literals, or a collection of
       string literals
    :param caseless: treat all literals as caseless
    :param use_regex: bool - as an optimization, will
       generate a :class:`Regex` object; otherwise, will generate
       a :class:`MatchFirst` object (if ``caseless=True`` or
       ``as_keyword=True``, or if creating a :class:`Regex` raises an exception)
    :param as_keyword: bool - enforce :class:`Keyword`-style matching on the
       generated expressions

    Parameters ``asKeyword`` and ``useRegex`` are retained for pre-PEP8
    compatibility, but will be removed in a future release.

    Example:

    .. testcode::

       comp_oper = one_of("< = > <= >= !=")
       var = Word(alphas)
       number = Word(nums)
       term = var | number
       comparison_expr = term + comp_oper + term
       print(comparison_expr.search_string("B = 12  AA=23 B<=AA AA>12"))

    prints:

    .. testoutput::

       [['B', '=', '12'], ['AA', '=', '23'], ['B', '<=', 'AA'], ['AA', '>', '12']]
    """
    useRegex: bool = deprecate_argument(kwargs, "useRegex", True)
    asKeyword: bool = deprecate_argument(kwargs, "asKeyword", False)

    asKeyword = asKeyword or as_keyword
    useRegex = useRegex and use_regex

    if (
        isinstance(caseless, str_type)
        and __diag__.warn_on_multiple_string_args_to_oneof
    ):
        warnings.warn(
            "warn_on_multiple_string_args_to_oneof:"
            " More than one string argument passed to one_of, pass"
            " choices as a list or space-delimited string",
            PyparsingDiagnosticWarning,
            stacklevel=2,
        )

    if caseless:
        is_equal = lambda a, b: a.upper() == b.upper()
        masks = lambda a, b: b.upper().startswith(a.upper())
    else:
        is_equal = operator.eq
        masks = lambda a, b: b.startswith(a)

    symbols: list[str]
    if isinstance(strs, str_type):
        strs = typing.cast(str, strs)
        symbols = strs.split()
    elif isinstance(strs, Iterable):
        symbols = list(strs)
    else:
        raise TypeError("Invalid argument to one_of, expected string or iterable")
    if not symbols:
        return NoMatch()

    # reorder given symbols to take care to avoid masking longer choices with shorter ones
    # (but only if the given symbols are not just single characters)
    i = 0
    while i < len(symbols) - 1:
        cur = symbols[i]
        for j, other in enumerate(symbols[i + 1 :]):
            if is_equal(other, cur):
                del symbols[i + j + 1]
                break
            if len(other) > len(cur) and masks(cur, other):
                del symbols[i + j + 1]
                symbols.insert(i, other)
                break
        else:
            i += 1

    if useRegex:
        re_flags: int = re.IGNORECASE if caseless else 0

        try:
            if all(len(sym) == 1 for sym in symbols):
                # symbols are just single characters, create range regex pattern
                patt = f"[{''.join(_escape_regex_range_chars(sym) for sym in symbols)}]"
            else:
                patt = "|".join(re.escape(sym) for sym in symbols)

            # wrap with \b word break markers if defining as keywords
            if asKeyword:
                patt = rf"\b(?:{patt})\b"

            ret = Regex(patt, flags=re_flags)
            ret.set_name(" | ".join(repr(s) for s in symbols))

            if caseless:
                # add parse action to return symbols as specified, not in random
                # casing as found in input string
                symbol_map = {sym.lower(): sym for sym in symbols}
                ret.add_parse_action(lambda s, l, t: symbol_map[t[0].lower()])

            return ret

        except re.error:
            warnings.warn(
                "Exception creating Regex for one_of, building MatchFirst",
                PyparsingDiagnosticWarning,
                stacklevel=2,
            )

    # last resort, just use MatchFirst of Token class corresponding to caseless
    # and asKeyword settings
    CASELESS = KEYWORD = True
    parse_element_class = {
        (CASELESS, KEYWORD): CaselessKeyword,
        (CASELESS, not KEYWORD): CaselessLiteral,
        (not CASELESS, KEYWORD): Keyword,
        (not CASELESS, not KEYWORD): Literal,
    }[(caseless, asKeyword)]
    return MatchFirst(parse_element_class(sym) for sym in symbols).set_name(
        " | ".join(symbols)
    )


def oneOf(strs, caseless=False, useRegex=True, asKeyword=False):
    """Helper to quickly define a set of alternative Literals, and makes
    sure to do longest-first testing when there is a conflict,
    regardless of the input order, but returns
    a :class:`MatchFirst` for best performance.

    Parameters:

     - strs - a string of space-delimited literals, or a collection of
       string literals
     - caseless - (default= ``False``) - treat all literals as
       caseless
     - useRegex - (default= ``True``) - as an optimization, will
       generate a Regex object; otherwise, will generate
       a :class:`MatchFirst` object (if ``caseless=True`` or ``asKeyword=True``, or if
       creating a :class:`Regex` raises an exception)
     - asKeyword - (default=``False``) - enforce Keyword-style matching on the
       generated expressions

    Example::

        comp_oper = oneOf("< = > <= >= !=")
        var = Word(alphas)
        number = Word(nums)
        term = var | number
        comparison_expr = term + comp_oper + term
        print(comparison_expr.searchString("B = 12  AA=23 B<=AA AA>12"))

    prints::

        [['B', '=', '12'], ['AA', '=', '23'], ['B', '<=', 'AA'], ['AA', '>', '12']]
    """
    if isinstance(caseless, basestring):
        warnings.warn("More than one string argument passed to oneOf, pass "
                      "choices as a list or space-delimited string", stacklevel=2)

    if caseless:
        isequal = (lambda a, b: a.upper() == b.upper())
        masks = (lambda a, b: b.upper().startswith(a.upper()))
        parseElementClass = CaselessKeyword if asKeyword else CaselessLiteral
    else:
        isequal = (lambda a, b: a == b)
        masks = (lambda a, b: b.startswith(a))
        parseElementClass = Keyword if asKeyword else Literal

    symbols = []
    if isinstance(strs, basestring):
        symbols = strs.split()
    elif isinstance(strs, Iterable):
        symbols = list(strs)
    else:
        warnings.warn("Invalid argument to oneOf, expected string or iterable",
                      SyntaxWarning, stacklevel=2)
    if not symbols:
        return NoMatch()

    if not asKeyword:
        # if not producing keywords, need to reorder to take care to avoid masking
        # longer choices with shorter ones
        i = 0
        while i < len(symbols) - 1:
            cur = symbols[i]
            for j, other in enumerate(symbols[i + 1:]):
                if isequal(other, cur):
                    del symbols[i + j + 1]
                    break
                elif masks(cur, other):
                    del symbols[i + j + 1]
                    symbols.insert(i, other)
                    break
            else:
                i += 1

    if not (caseless or asKeyword) and useRegex:
        # ~ print (strs, "->", "|".join([_escapeRegexChars(sym) for sym in symbols]))
        try:
            if len(symbols) == len("".join(symbols)):
                return Regex("[%s]" % "".join(_escapeRegexRangeChars(sym) for sym in symbols)).setName(' | '.join(symbols))
            else:
                return Regex("|".join(re.escape(sym) for sym in symbols)).setName(' | '.join(symbols))
        except Exception:
            warnings.warn("Exception creating Regex for oneOf, building MatchFirst",
                    SyntaxWarning, stacklevel=2)

    # last resort, just use MatchFirst
    return MatchFirst(parseElementClass(sym) for sym in symbols).setName(' | '.join(symbols))

