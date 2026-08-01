
def linkify(text, callbacks=DEFAULT_CALLBACKS, skip_tags=None, parse_email=False):
    """Convert URL-like strings in an HTML fragment to links

    This function converts strings that look like URLs, domain names and email
    addresses in text that may be an HTML fragment to links, while preserving:

    1. links already in the string
    2. urls found in attributes
    3. email addresses

    linkify does a best-effort approach and tries to recover from bad
    situations due to crazy text.

    .. Note::

       If you're linking a lot of text and passing the same argument values or
       you want more configurability, consider using a
       :py:class:`bleach.linkifier.Linker` instance.

    .. Note::

       If you have text that you want to clean and then linkify, consider using
       the :py:class:`bleach.linkifier.LinkifyFilter` as a filter in the clean
       pass. That way you're not parsing the HTML twice.

    :arg str text: the text to linkify

    :arg list callbacks: list of callbacks to run when adjusting tag attributes;
        defaults to ``bleach.linkifier.DEFAULT_CALLBACKS``

    :arg list skip_tags: list of tags that you don't want to linkify the
        contents of; for example, you could set this to ``['pre']`` to skip
        linkifying contents of ``pre`` tags

    :arg bool parse_email: whether or not to linkify email addresses

    :returns: linkified text as unicode

    """
    linker = Linker(callbacks=callbacks, skip_tags=skip_tags, parse_email=parse_email)
    return linker.linkify(text)


def linkify(state: StateCore) -> None:
    """Rule for identifying plain-text links."""
    if not state.md.options.linkify:
        return

    if not state.md.linkify:
        raise ModuleNotFoundError("Linkify enabled but not installed.")

    for inline_token in state.tokens:
        if inline_token.type != "inline" or not state.md.linkify.pretest(
            inline_token.content
        ):
            continue

        tokens = inline_token.children

        htmlLinkLevel = 0

        # We scan from the end, to keep position when new tags added.
        # Use reversed logic in links start/end match
        assert tokens is not None
        i = len(tokens)
        while i >= 1:
            i -= 1
            assert isinstance(tokens, list)
            currentToken = tokens[i]

            # Skip content of markdown links
            if currentToken.type == "link_close":
                i -= 1
                while (
                    tokens[i].level != currentToken.level
                    and tokens[i].type != "link_open"
                ):
                    i -= 1
                continue

            # Skip content of html tag links
            if currentToken.type == "html_inline":
                if isLinkOpen(currentToken.content) and htmlLinkLevel > 0:
                    htmlLinkLevel -= 1
                if isLinkClose(currentToken.content):
                    htmlLinkLevel += 1
            if htmlLinkLevel > 0:
                continue

            if currentToken.type == "text" and state.md.linkify.test(
                currentToken.content
            ):
                text = currentToken.content
                links: list[_LinkType] = state.md.linkify.match(text) or []

                # Now split string to nodes
                nodes = []
                level = currentToken.level
                lastPos = 0

                # forbid escape sequence at the start of the string,
                # this avoids http\://example.com/ from being linkified as
                # http:<a href="//example.com/">//example.com/</a>
                if (
                    links
                    and links[0].index == 0
                    and i > 0
                    and tokens[i - 1].type == "text_special"
                ):
                    links = links[1:]

                for link in links:
                    url = link.url
                    fullUrl = state.md.normalizeLink(url)
                    if not state.md.validateLink(fullUrl):
                        continue

                    urlText = link.text

                    # Linkifier might send raw hostnames like "example.com", where url
                    # starts with domain name. So we prepend http:// in those cases,
                    # and remove it afterwards.
                    if not link.schema:
                        urlText = HTTP_RE.sub(
                            "", state.md.normalizeLinkText("http://" + urlText)
                        )
                    elif link.schema == "mailto:" and TEST_MAILTO_RE.search(urlText):
                        urlText = MAILTO_RE.sub(
                            "", state.md.normalizeLinkText("mailto:" + urlText)
                        )
                    else:
                        urlText = state.md.normalizeLinkText(urlText)

                    pos = link.index

                    if pos > lastPos:
                        token = Token("text", "", 0)
                        token.content = text[lastPos:pos]
                        token.level = level
                        nodes.append(token)

                    token = Token("link_open", "a", 1)
                    token.attrs = {"href": fullUrl}
                    token.level = level
                    level += 1
                    token.markup = "linkify"
                    token.info = "auto"
                    nodes.append(token)

                    token = Token("text", "", 0)
                    token.content = urlText
                    token.level = level
                    nodes.append(token)

                    token = Token("link_close", "a", -1)
                    level -= 1
                    token.level = level
                    token.markup = "linkify"
                    token.info = "auto"
                    nodes.append(token)

                    lastPos = link.last_index

                if lastPos < len(text):
                    token = Token("text", "", 0)
                    token.content = text[lastPos:]
                    token.level = level
                    nodes.append(token)

                inline_token.children = tokens = arrayReplaceAt(tokens, i, nodes)


def linkify(state: StateInline, silent: bool) -> bool:
    """Rule for identifying plain-text links."""
    if not state.md.options.linkify:
        return False
    if state.linkLevel > 0:
        return False
    if not state.md.linkify:
        raise ModuleNotFoundError("Linkify enabled but not installed.")

    pos = state.pos
    maximum = state.posMax

    if (
        (pos + 3) > maximum
        or state.src[pos] != ":"
        or state.src[pos + 1] != "/"
        or state.src[pos + 2] != "/"
    ):
        return False

    if not (match := SCHEME_RE.search(state.pending)):
        return False

    proto = match.group(1)
    if not (link := state.md.linkify.match_at_start(state.src[pos - len(proto) :])):
        return False
    url: str = link.url

    # disallow '*' at the end of the link (conflicts with emphasis)
    url = url.rstrip("*")

    full_url = state.md.normalizeLink(url)
    if not state.md.validateLink(full_url):
        return False

    if not silent:
        state.pending = state.pending[: -len(proto)]

        token = state.push("link_open", "a", 1)
        token.attrs = {"href": full_url}
        token.markup = "linkify"
        token.info = "auto"

        token = state.push("text", "", 0)
        token.content = state.md.normalizeLinkText(url)

        token = state.push("link_close", "a", -1)
        token.markup = "linkify"
        token.info = "auto"

    state.pos += len(url) - len(proto)
    return True

