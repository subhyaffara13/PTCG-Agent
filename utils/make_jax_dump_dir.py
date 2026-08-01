
def make_jax_dump_dir(out_dir_path: str) -> pathlib.Path | None:
  """Make a directory or return the undeclared outputs directory if `sponge`."""
  if not out_dir_path:
    return None
  if out_dir_path == "sponge":
    out_dir_path = os.environ.get("TEST_UNDECLARED_OUTPUTS_DIR", "")
    if not out_dir_path:
      raise ValueError(
          "Got output directory (e.g., via JAX_DUMP_IR_TO) 'sponge' but"
          " TEST_UNDECLARED_OUTPUTS_DIR is not defined."
      )
  out_dir = Path(out_dir_path)
  out_dir.mkdir(parents=True, exist_ok=True)
  return cast(pathlib.Path, out_dir)

