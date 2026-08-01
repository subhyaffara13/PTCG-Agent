
def set_up_pydantic() -> None:
  """Registers handlers for pydantic types."""
  if pydantic is None:
    raise RuntimeError(
        "Cannot set up pydantic support in treescope: pydantic cannot be"
        " imported."
    )
  type_registries.TREESCOPE_HANDLER_REGISTRY[pydantic.BaseModel] = (
      render_pydantic_model
  )

