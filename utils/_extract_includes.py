
def _extract_includes(contents: str) -> list[tuple[bool, str]]:
    """Return each `#include` directive's (is_angled, name) from `contents`.

    is_angled=False for `#include "foo"`, True for `#include <foo>`.
    """
    out: list[tuple[bool, str]] = []
    for quoted, angled in _INCLUDE_RE.findall(contents):
        if quoted:
            out.append((False, quoted))
        else:
            out.append((True, angled))
    return out

