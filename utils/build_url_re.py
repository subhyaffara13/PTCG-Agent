import re

def build_url_re(tlds=TLDS, protocols=html5lib_shim.allowed_protocols):
    """Builds the url regex used by linkifier

    If you want a different set of tlds or allowed protocols, pass those in
    and stomp on the existing ``url_re``::

        from bleach import linkifier

        my_url_re = linkifier.build_url_re(my_tlds_list, my_protocols)

        linker = LinkifyFilter(url_re=my_url_re)

    """
    return re.compile(
        r"""\(*  # Match any opening parentheses.
        \b(?<![@.])(?:(?:{0}):/{{0,3}}(?:(?:\w+:)?\w+@)?)?  # http://
        ([\w-]+\.)+(?:{1})(?:\:[0-9]+)?(?!\.\w)\b   # xx.yy.tld(:##)?
        (?:[/?][^\s\{{\}}\|\\\^`<>"]*)?
            # /path/zz (excluding "unsafe" chars from RFC 3986,
            # except for # and ~, which happen in practice)
        """.format("|".join(sorted(protocols)), "|".join(sorted(tlds))),
        re.IGNORECASE | re.VERBOSE | re.UNICODE,
    )

