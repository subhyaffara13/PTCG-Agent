
def add_alias(
    the_object: Any,
    path: ModuleAttributePath,
    on_conflict: Literal["ignore", "overwrite", "warn", "error"] = "warn",
):
  """Adds an alias to this object.

  Args:
    the_object: Object to add an alias to.
    path: The path where we expect to find this object.
    on_conflict: What to do if we try to add an alias for an object that already
      has one.

  Raises:
    ValueError: If overwrite is False and this object already has an alias,
      or if this object is not accessible at this path.
  """
  alias_env = _alias_environment.get()
  if id(the_object) in alias_env.aliases:
    if on_conflict == "ignore":
      return
    elif on_conflict == "overwrite":
      pass  # Continue adding an alias
    elif on_conflict == "warn":
      warnings.warn(
          f"Not defining alias {path} for {the_object!r}: it already has an"
          f" alias {alias_env.aliases[id(the_object)]}."
      )
    elif on_conflict == "error":
      raise ValueError(
          f"Can't define alias {path} for {the_object!r}: it already has an"
          f" alias {alias_env.aliases[id(the_object)]}."
      )

  retrieved = path.retrieve()
  if retrieved is not the_object:
    raise ValueError(
        f"Can't define alias {path} for {the_object!r}: {path} "
        f" is a different object {retrieved!r}."
    )
  # OK, it's probably safe to add this object as a well-known alias.
  alias_env.aliases[id(the_object)] = path

