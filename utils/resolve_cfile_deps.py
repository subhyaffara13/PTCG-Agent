import os

def resolve_cfile_deps(
    cfile_dir: str, direct_includes: list[tuple[bool, str]], target_dir: str
) -> set[str]:
    """
    Resolve a .c file's `#include`s to on-disk paths, walking transitively through resolved headers.

    The C preprocessor resolves `#include "foo"` against the includer's directory first, then via
    -I, while `#include <foo>` only uses -I. We mirror that exactly: quoted includes are searched
    in (includer_dir, target_dir) order, and angled includes are searched in target_dir only.
    `target_dir` is the only -I path that holds files we generate; anything we cannot resolve under
    it (or, for quoted form, the includer's dir) is dropped. Other headers like `<Python.h>` and
    `<CPy.h>` live elsewhere and do not change between builds, so they are not real dependencies
    for incremental purposes.

    The walk is transitive: each resolved header is opened and scanned for its own `#include`
    directives. Without this, cross-group export-table headers reached via `__native_internal_<mod>.h`
    (which includes `<other_group/__native_other.h>`) would be missed, and edits that shift struct
    offsets in `other_group` would not trigger a recompile of the consumer's .o file. Its baked-in
    offsets would then resolve to whatever class/function now occupies that slot => runtime corruption.

    Returns a set of resolved paths suitable for use as an Extension.depends list.
    """
    resolved: set[str] = set()

    # Worklist of (search_dir, is_angled, header_name). search_dir is the includer's directory; for the
    # initial cfile it is the cfile's dir, for a transitively-included header it is that header's dir.
    # It is only consulted for quoted-form includes.
    worklist: list[tuple[str, bool, str]] = [
        (cfile_dir, is_angled, dep) for is_angled, dep in direct_includes
    ]

    while worklist:
        search_dir, is_angled, dep = worklist.pop()
        # Quoted form: includer's dir first, then -I (target_dir).
        # Angled form: -I only (skips the includer's dir).
        search_bases = (target_dir,) if is_angled else (search_dir, target_dir)
        for base in search_bases:
            candidate = os.path.normpath(os.path.join(base, dep))
            if not os.path.exists(candidate):
                continue
            if candidate in resolved:
                break
            resolved.add(candidate)
            # Recurse only into headers. Some lib-rt sources are pulled in as `#include "init.c"` etc.;
            # those do not resolve under target_dir so they get filtered out before we would try to scan
            # them, but the .h guard is a cheap belt-and-braces.
            if candidate.endswith(".h"):
                try:
                    with open(candidate, encoding="utf-8") as f:
                        header_contents = f.read()
                except OSError:
                    header_contents = ""
                sub_dir = os.path.dirname(candidate)
                for sub_angled, sub in _extract_includes(header_contents):
                    worklist.append((sub_dir, sub_angled, sub))
            break
    return resolved

