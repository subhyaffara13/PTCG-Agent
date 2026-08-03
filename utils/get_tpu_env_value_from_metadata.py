import re

def get_tpu_env_value_from_metadata(key) -> str | None:
  metadata_value = None
  tpu_env_data = get_metadata('tpu-env')[0]
  key_value_pairs = tpu_env_data.split('\n')
  for key_value_pair in key_value_pairs:
    # Typical line is MEGASCALE_NUM_SLICES: '2'
    if ':' in key_value_pair:
      row_key, value = re.split(':', key_value_pair, 1)
      row_key = row_key.strip()
      if row_key == key:
        metadata_value = value.strip().strip("'")
  return metadata_value

