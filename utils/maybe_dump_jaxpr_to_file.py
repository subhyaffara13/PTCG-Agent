import logging

def maybe_dump_jaxpr_to_file(
    fun_name: str, jaxpr: core.Jaxpr
) -> str | None:
  """Maybe dumps the `jaxpr` to a file.

  Dumps the jaxpr if JAX_DUMP_JAXPR_TO is defined.

  Args:
    fn: The name of the function whose jaxpr is being dumped.
    jaxpr: The jaxpr to dump.

  Returns:
    The path to the file where the jaxpr was dumped, or None if no file was
    dumped.
  """
  if not (out_dir := path.make_jax_dump_dir(config.jax_dump_ir_to.value)):
    return None
  modes = config.jax_dump_ir_modes.value.split(",")
  if (
      "jaxpr" not in modes
      and "jaxpr_html" not in modes
      and "eqn_count_pprof" not in modes
  ):
    return None
  id = next(_jaxpr_id_counter)
  if "jaxpr" in modes:
    logging.log(
        logging.INFO, "Dumping jaxpr for %s to %s.", fun_name, out_dir
    )
    jaxpr_path = out_dir / f"jax_{id:06d}_{fun_name}.jaxpr.txt"
    jaxpr_path.write_text(jaxpr.pretty_print())
  if "jaxpr_html" in modes:
    logging.log(
        logging.INFO, "Dumping jaxpr HTML for %s to %s.", fun_name, out_dir
    )
    html_path = out_dir / f"jax_{id:06d}_{fun_name}.jaxpr.html"
    html_path.write_text(jaxpr_to_html(jaxpr))
  if "eqn_count_pprof" in modes:
    logging.log(
        logging.INFO, "Dumping eqn count pprof for %s to %s.", fun_name, out_dir
    )
    eqn_prof_path = out_dir / f"jax_{id:06d}_{fun_name}.eqn_count_pprof"
    eqn_prof_path.write_bytes(pprof_equation_profile(jaxpr))
  return fun_name

