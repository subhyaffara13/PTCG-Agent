import re

def build_email_re(tlds=TLDS):
    """Builds the email regex used by linkifier

    If you want a different set of tlds, pass those in and stomp on the existing ``email_re``::

        from bleach import linkifier

        my_email_re = linkifier.build_email_re(my_tlds_list)

        linker = LinkifyFilter(email_re=my_url_re)

    """
    # open and closing braces doubled below for format string
    return re.compile(
        r"""(?<!//)
        (([-!#$%&'*+/=?^_`{{}}|~0-9A-Z]+
            (\.[-!#$%&'*+/=?^_`{{}}|~0-9A-Z]+)*  # dot-atom
        |^"([\001-\010\013\014\016-\037!#-\[\]-\177]
            |\\[\001-\011\013\014\016-\177])*"  # quoted-string
        )@(?:[A-Z0-9](?:[A-Z0-9-]{{0,61}}[A-Z0-9])?\.)+(?:{0}))  # domain
        """.format("|".join(tlds)),
        re.IGNORECASE | re.MULTILINE | re.VERBOSE,
    )

