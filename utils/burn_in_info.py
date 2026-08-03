import json

def burn_in_info(skeleton, info):
    """Burn model info into the HTML skeleton.

    The result will render the hard-coded model info and
    have no external network dependencies for code or data.
    """

    # Note that Python's json serializer does not escape slashes in strings.
    # Since we're inlining this JSON directly into a script tag, a string
    # containing "</script>" would end the script prematurely and
    # mess up our page.  Unconditionally escape fixes that.
    return skeleton.replace(
        "BURNED_IN_MODEL_INFO = null",
        "BURNED_IN_MODEL_INFO = " + json.dumps(info, sort_keys=True).replace("/", "\\/"))

