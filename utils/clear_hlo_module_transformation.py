
def clear_hlo_module_transformation(
    name: str,
    stage: PipelineStage = PipelineStage.PRE_SCHEDULER,
    platforms: Sequence[str] | str | None = None,
) -> bool:
  """Clear a registered custom compiler pass.

  Args:
    name: The name of the compiler pass to clear.
    stage: The pipeline stage of the pass. Must be a ``PipelineStage`` enum.
    platforms: The list of platforms to clear the pass for. If ``None``, the
      pass is cleared for all known backends.

  Returns:
    True if the pass was found and cleared, False otherwise.
  """
  if _xla is None:
    raise NotImplementedError(
        "clear_hlo_module_transformation requires jaxlib version >= 0.10.2"
    )
  if not isinstance(stage, PipelineStage):
    raise TypeError(f"stage must be a PipelineStage enum, got {type(stage)}")
  stage_int = stage.value

  if platforms is None:
    platforms_list = ["cpu"] + list(xla_bridge._backend_factories.keys())
    platforms_list = list(dict.fromkeys(platforms_list))
  elif isinstance(platforms, str):
    platforms_list = [platforms]
  else:
    platforms_list = list(dict.fromkeys(platforms))

  cleared = False
  if "cpu" in platforms_list:
    cleared |= _xla.clear_xla_transform(name, stage_int)

  # Also clear on initialized plugin clients.
  for platform in platforms_list:
    if platform != "cpu":
      try:
        initialized_backends = xla_bridge.backends()
        if platform in initialized_backends:
          client = initialized_backends[platform]
          cleared |= _xla.clear_xla_transform_c_api(client, name, stage_int)
      except RuntimeError:
        pass
      except ValueError:
        pass

  return cleared

