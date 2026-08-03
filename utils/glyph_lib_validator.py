from typing import Any, Optional

def glyphLibValidator(value: Any) -> tuple[bool, Optional[str]]:
    """
    Check the validity of the lib.
    Version 3+ (though it's backwards compatible with UFO 1 and UFO 2).

    >>> lib = {"foo" : "bar"}
    >>> glyphLibValidator(lib)
    (True, None)

    >>> lib = {"public.awesome" : "hello"}
    >>> glyphLibValidator(lib)
    (True, None)

    >>> lib = {"public.markColor" : "1,0,0,0.5"}
    >>> glyphLibValidator(lib)
    (True, None)

    >>> lib = {"public.markColor" : 1}
    >>> valid, msg = glyphLibValidator(lib)
    >>> valid
    False
    >>> print(msg)
    public.markColor is not properly formatted.
    """
    if not isDictEnough(value):
        reason = "expected a dictionary, found %s" % type(value).__name__
        return False, _bogusLibFormatMessage % reason
    for key, value in value.items():
        if not isinstance(key, str):
            reason = "key (%s) should be a string" % key
            return False, _bogusLibFormatMessage % reason
        # public.markColor
        if key == "public.markColor":
            if not colorValidator(value):
                return False, "public.markColor is not properly formatted."
    return True, None

