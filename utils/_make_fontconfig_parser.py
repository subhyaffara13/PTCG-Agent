from typing import Optional

def _make_fontconfig_parser():
    def comma_separated(elem):
        return elem + ZeroOrMore(Suppress(",") + elem)

    family = Regex(fr"([^{_family_punc}]|(\\[{_family_punc}]))*")
    size = Regex(r"([0-9]+\.?[0-9]*|\.[0-9]+)")
    name = Regex(r"[a-z]+")
    value = Regex(fr"([^{_value_punc}]|(\\[{_value_punc}]))*")
    prop = Group((name + Suppress("=") + comma_separated(value)) | one_of(_CONSTANTS))
    return (
        Optional(comma_separated(family)("families"))
        + Optional("-" + comma_separated(size)("sizes"))
        + ZeroOrMore(":" + prop("properties*"))
        + StringEnd()
    )

