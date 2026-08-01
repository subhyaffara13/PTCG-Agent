
def maybe_qualified_type_name(ty: type[Any]) -> RenderableTreePart:
  """Formats the name of a type so that it is qualified in roundtrip mode.

  Args:
    ty: A type object to render.

  Returns:
    A tree part that renders as a fully-qualified name in roundtrip mode, or as
    the simple class name otherwise. Module names will be either inferred from
    the type's definition or looked up using `canonical_aliases`.
  """
  class_name = ty.__name__

  alias = canonical_aliases.lookup_alias(
      ty, allow_outdated=True, allow_relative=True
  )
  if alias:
    access_path = str(alias)
  else:
    access_path = f"<unknown>.{class_name}"

  if access_path.endswith(class_name):
    return basic_parts.siblings(
        basic_parts.RoundtripCondition(
            roundtrip=common_styles.QualifiedTypeNameSpanGroup(
                basic_parts.Text(access_path.removesuffix(class_name))
            )
        ),
        basic_parts.Text(class_name),
    )
  else:
    return basic_parts.RoundtripCondition(
        roundtrip=basic_parts.Text(access_path),
        not_roundtrip=basic_parts.Text(class_name),
    )

