from typing import Any

def stable_hlo_generate_dump(args: tuple[Any, str],
                             **_) -> common.SourceMapDump:
  lowered, work_dir = args
  del work_dir
  hlo_text = lowered.as_text(debug_info=True)
  source_map = mlir.create_mlir_sourcemap(hlo_text)
  return common.SourceMapDump(
      source_map=source_map,
      generated_code=hlo_text,
      pass_name=HloPass.STABLE_HLO.value,
  )

