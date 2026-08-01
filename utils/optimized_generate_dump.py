
def optimized_generate_dump(args: tuple[Any, str],
                            xla_compiler_flags: dict[str, Any] | None = None,
                            **_) -> common.SourceMapDump:
  lowered, work_dir = args
  compilation_args = {"xla_dump_to": work_dir, **(xla_compiler_flags or {})}
  hlo_text = lowered.compile(compilation_args).as_text()
  source_map = parse_hlo_dump(hlo_text)
  return common.SourceMapDump(
      source_map=source_map,
      generated_code=hlo_text,
      pass_name=HloPass.OPTIMIZED.value,
  )

