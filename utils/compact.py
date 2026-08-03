import functools
import os

def compact(paths: Iterable[str]) -> set[str]:
    """Compact a path set to contain the minimal number of paths
    necessary to contain all paths in the set. If /a/path/ and
    /a/path/to/a/file.txt are both in the set, leave only the
    shorter path."""

    sep = os.path.sep
    short_paths: set[str] = set()
    for path in sorted(paths, key=len):
        should_skip = any(
            path.startswith(shortpath.rstrip("*"))
            and path[len(shortpath.rstrip("*").rstrip(sep))] == sep
            for shortpath in short_paths
        )
        if not should_skip:
            short_paths.add(path)
    return short_paths


def compact(font: TTFont, level: int) -> TTFont:
    # Ideal plan:
    #  1. Find lookups of Lookup Type 2: Pair Adjustment Positioning Subtable
    #     https://docs.microsoft.com/en-us/typography/opentype/spec/gpos#lookup-type-2-pair-adjustment-positioning-subtable
    #  2. Extract glyph-glyph kerning and class-kerning from all present subtables
    #  3. Regroup into different subtable arrangements
    #  4. Put back into the lookup
    #
    # Actual implementation:
    #  2. Only class kerning is optimized currently
    #  3. If the input kerning is already in several subtables, the subtables
    #     are not grouped together first; instead each subtable is treated
    #     independently, so currently this step is:
    #     Split existing subtables into more smaller subtables
    gpos = font.get("GPOS")

    # If the font does not contain a GPOS table, there is nothing to do.
    if gpos is None:
        return font

    for lookup in gpos.table.LookupList.Lookup:
        if lookup.LookupType == 2:
            compact_lookup(font, level, lookup)
        elif lookup.LookupType == 9 and lookup.SubTable[0].ExtensionLookupType == 2:
            compact_ext_lookup(font, level, lookup)

    return font


def compact(fun: _CallableT) -> _CallableT:
  """Marks the given module method allowing inlined submodules.

  Methods wrapped in @compact can define submodules directly within the method.

  For instance::

    >>> import flax.linen as nn

    >>> class Foo(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x, features):
    ...     x = nn.Dense(features)(x)
    ...     ...
    ...     return x

  At most one method in each Module may be wrapped with @compact.

  Args:
    fun: The Module method to mark as compact.

  Returns:
    The given function ``fun`` marked as compact.
  """
  fun.compact = True  # type: ignore[attr-defined]
  return fun


def compact(f: F) -> F:
  @functools.wraps(f)
  def compact_wrapper(self, *args, **kwargs):
    if not isinstance(self, Module):
      raise ValueError(
        f"Expected 'self' to be a nnx.bridge.Module, got {type(self).__name__}"
      )

    MODULE_CONTEXT.module_stack.append(ModuleStackEntry(self, in_compact=True))

    try:
      return f(self, *args, **kwargs)
    finally:
      MODULE_CONTEXT.module_stack.pop()

  return compact_wrapper  # type: ignore

