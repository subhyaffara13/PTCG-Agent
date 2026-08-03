import logging
import os

def _configure_hlo_dump(output_directory: str):
  """Sets the XLA_FLAGS environment variable to enable HLO dumping."""
  hlo_dump_path = epath.Path(output_directory) / 'hlo_dump'
  try:
    hlo_dump_path.mkdir(parents=True, exist_ok=True)
    logging.info('Created HLO dump directory: %s', hlo_dump_path)
  except OSError as e:
    logging.exception(
        'Failed to create HLO dump directory %s: %s', hlo_dump_path, e
    )
    raise

  xla_flags = os.environ.get('XLA_FLAGS', '')
  # Options: as_proto, as_text, as_url
  dump_flags = f'--xla_dump_to={hlo_dump_path} --xla_dump_hlo_as_proto'

  new_xla_flags = f'{xla_flags} {dump_flags}'.strip()
  os.environ['XLA_FLAGS'] = new_xla_flags
  logging.info('Set XLA_FLAGS for HLO dump: %s', new_xla_flags)

