
def original_hlo_generate_dump(args: tuple[Any, str],
                               **_) -> common.SourceMapDump:
  lowered, work_dir = args
  del work_dir
  hlo_text = lowered.as_text(dialect="hlo", debug_info=True)
  source_map = parse_hlo_dump(hlo_text)
  return common.SourceMapDump(
      source_map=source_map,
      generated_code=hlo_text,
      pass_name=HloPass.ORIGINAL.value,
  )

