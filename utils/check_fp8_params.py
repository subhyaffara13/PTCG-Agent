
def check_fp8_params(params):
  # Check if all required keys are present
  missing_keys = set(fp8_params_keys) - set(params)
  if missing_keys:
    raise ValueError(f"The following keys are missing from fp8_params: {', '.join(missing_keys)}")

