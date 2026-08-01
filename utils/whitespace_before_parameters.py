
def whitespace_before_parameters(logical_line, tokens):
    r"""Avoid extraneous whitespace.

    Avoid extraneous whitespace in the following situations:
    - before the open parenthesis that starts the argument list of a
      function call.
    - before the open parenthesis that starts an indexing or slicing.

    Okay: spam(1)
    E211: spam (1)

    Okay: dict['key'] = list[index]
    E211: dict ['key'] = list[index]
    E211: dict['key'] = list [index]
    """
    prev_type, prev_text, __, prev_end, __ = tokens[0]
    for index in range(1, len(tokens)):
        token_type, text, start, end, __ = tokens[index]
        if (
            token_type == tokenize.OP and
            text in '([' and
            start != prev_end and
            (prev_type == tokenize.NAME or prev_text in '}])') and
            # Syntax "class A (B):" is allowed, but avoid it
            (index < 2 or tokens[index - 2][1] != 'class') and
            # Allow "return (a.foo for a in range(5))"
            not keyword.iskeyword(prev_text) and
            (
                # 3.12+: type is a soft keyword but no braces after
                prev_text == 'type' or
                not keyword.issoftkeyword(prev_text)
            )
        ):
            yield prev_end, "E211 whitespace before '%s'" % text
        prev_type = token_type
        prev_text = text
        prev_end = end

