
def _postProcess(state: StateInline, delimiters: list[Delimiter]) -> None:
    i = len(delimiters) - 1
    while i >= 0:
        startDelim = delimiters[i]

        # /* _ */  /* * */
        if startDelim.marker != 0x5F and startDelim.marker != 0x2A:
            i -= 1
            continue

        # Process only opening markers
        if startDelim.end == -1:
            i -= 1
            continue

        endDelim = delimiters[startDelim.end]

        # If the previous delimiter has the same marker and is adjacent to this one,
        # merge those into one strong delimiter.
        #
        # `<em><em>whatever</em></em>` -> `<strong>whatever</strong>`
        #
        isStrong = (
            i > 0
            and delimiters[i - 1].end == startDelim.end + 1
            # check that first two markers match and adjacent
            and delimiters[i - 1].marker == startDelim.marker
            and delimiters[i - 1].token == startDelim.token - 1
            # check that last two markers are adjacent (we can safely assume they match)
            and delimiters[startDelim.end + 1].token == endDelim.token + 1
        )

        ch = chr(startDelim.marker)

        token = state.tokens[startDelim.token]
        token.type = "strong_open" if isStrong else "em_open"
        token.tag = "strong" if isStrong else "em"
        token.nesting = 1
        token.markup = ch + ch if isStrong else ch
        token.content = ""

        token = state.tokens[endDelim.token]
        token.type = "strong_close" if isStrong else "em_close"
        token.tag = "strong" if isStrong else "em"
        token.nesting = -1
        token.markup = ch + ch if isStrong else ch
        token.content = ""

        if isStrong:
            state.tokens[delimiters[i - 1].token].content = ""
            state.tokens[delimiters[startDelim.end + 1].token].content = ""
            i -= 1

        i -= 1


def _postProcess(state: StateInline, delimiters: list[Delimiter]) -> None:
    loneMarkers = []
    maximum = len(delimiters)
    single_tilde = state.md.options.get("strikethrough_single_tilde", False)

    i = 0
    while i < maximum:
        startDelim = delimiters[i]

        if startDelim.marker != 0x7E:  # /* ~ */
            i += 1
            continue

        if startDelim.end == -1:
            i += 1
            continue

        endDelim = delimiters[startDelim.end]

        # In single-tilde mode, opener and closer must have the same width
        # (both `~` or both `~~`).  The width is stored in the text token.
        if single_tilde:
            opener_content = state.tokens[startDelim.token].content
            closer_content = state.tokens[endDelim.token].content
            if opener_content != closer_content:
                i += 1
                continue

        markup = state.tokens[startDelim.token].content

        token = state.tokens[startDelim.token]
        token.type = "s_open"
        token.tag = "s"
        token.nesting = 1
        token.markup = markup
        token.content = ""

        token = state.tokens[endDelim.token]
        token.type = "s_close"
        token.tag = "s"
        token.nesting = -1
        token.markup = markup
        token.content = ""

        if (
            state.tokens[endDelim.token - 1].type == "text"
            and state.tokens[endDelim.token - 1].content == "~"
        ):
            loneMarkers.append(endDelim.token - 1)

        i += 1

    # If a marker sequence has an odd number of characters, it's split
    # like this: `~~~~~` -> `~` + `~~` + `~~`, leaving one marker at the
    # start of the sequence.
    #
    # So, we have to move all those markers after subsequent s_close tags.
    #
    while loneMarkers:
        i = loneMarkers.pop()
        j = i + 1

        while (j < len(state.tokens)) and (state.tokens[j].type == "s_close"):
            j += 1

        j -= 1

        if i != j:
            token = state.tokens[j]
            state.tokens[j] = state.tokens[i]
            state.tokens[i] = token

