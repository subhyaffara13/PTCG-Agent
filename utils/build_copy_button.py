
def build_copy_button(path: str | None) -> RenderableTreePart:
  """Builds a copy-path button, if `path` is provided and not empty."""
  if not path:
    return basic_parts.EmptyPart()
  else:
    return foldable_impl.StringCopyButton(
        annotation="Copy path: ", copy_string=path
    )

