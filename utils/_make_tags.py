from typing import Dict, Optional

def _makeTags(tagStr, xml, suppress_LT=Suppress("<"), suppress_GT=Suppress(">")):
    """Internal helper to construct opening and closing tag expressions,
    given a tag name"""
    if isinstance(tagStr, str_type):
        resname = tagStr
        tagStr = Keyword(tagStr, caseless=not xml)
    else:
        resname = tagStr.name

    tagAttrName = Word(alphas, alphanums + "_-:")
    if xml:
        tagAttrValue = dbl_quoted_string.copy().set_parse_action(remove_quotes)
        openTag = (
            suppress_LT
            + tagStr("tag")
            + Dict(ZeroOrMore(Group(tagAttrName + Suppress("=") + tagAttrValue)))
            + Opt("/", default=[False])("empty").set_parse_action(
                lambda s, l, t: t[0] == "/"
            )
            + suppress_GT
        )
    else:
        tagAttrValue = quoted_string.copy().set_parse_action(remove_quotes) | Word(
            printables, exclude_chars=">"
        )
        openTag = (
            suppress_LT
            + tagStr("tag")
            + Dict(
                ZeroOrMore(
                    Group(
                        tagAttrName.set_parse_action(lambda t: t[0].lower())
                        + Opt(Suppress("=") + tagAttrValue)
                    )
                )
            )
            + Opt("/", default=[False])("empty").set_parse_action(
                lambda s, l, t: t[0] == "/"
            )
            + suppress_GT
        )
    closeTag = Combine(Literal("</") + tagStr + ">", adjacent=False)

    openTag.set_name(f"<{resname}>")
    # add start<tagname> results name in parse action now that ungrouped names are not reported at two levels
    openTag.add_parse_action(
        lambda t: t.__setitem__(
            "start" + "".join(resname.replace(":", " ").title().split()), t.copy()
        )
    )
    closeTag = closeTag(
        "end" + "".join(resname.replace(":", " ").title().split())
    ).set_name(f"</{resname}>")
    openTag.tag = resname
    closeTag.tag = resname
    openTag.tag_body = SkipTo(closeTag())
    return openTag, closeTag


def _makeTags(tagStr, xml,
              suppress_LT=Suppress("<"),
              suppress_GT=Suppress(">")):
    """Internal helper to construct opening and closing tag expressions, given a tag name"""
    if isinstance(tagStr, basestring):
        resname = tagStr
        tagStr = Keyword(tagStr, caseless=not xml)
    else:
        resname = tagStr.name

    tagAttrName = Word(alphas, alphanums + "_-:")
    if xml:
        tagAttrValue = dblQuotedString.copy().setParseAction(removeQuotes)
        openTag = (suppress_LT
                   + tagStr("tag")
                   + Dict(ZeroOrMore(Group(tagAttrName + Suppress("=") + tagAttrValue)))
                   + Optional("/", default=[False])("empty").setParseAction(lambda s, l, t: t[0] == '/')
                   + suppress_GT)
    else:
        tagAttrValue = quotedString.copy().setParseAction(removeQuotes) | Word(printables, excludeChars=">")
        openTag = (suppress_LT
                   + tagStr("tag")
                   + Dict(ZeroOrMore(Group(tagAttrName.setParseAction(downcaseTokens)
                                           + Optional(Suppress("=") + tagAttrValue))))
                   + Optional("/", default=[False])("empty").setParseAction(lambda s, l, t: t[0] == '/')
                   + suppress_GT)
    closeTag = Combine(_L("</") + tagStr + ">", adjacent=False)

    openTag.setName("<%s>" % resname)
    # add start<tagname> results name in parse action now that ungrouped names are not reported at two levels
    openTag.addParseAction(lambda t: t.__setitem__("start" + "".join(resname.replace(":", " ").title().split()), t.copy()))
    closeTag = closeTag("end" + "".join(resname.replace(":", " ").title().split())).setName("</%s>" % resname)
    openTag.tag = resname
    closeTag.tag = resname
    openTag.tag_body = SkipTo(closeTag())
    return openTag, closeTag

