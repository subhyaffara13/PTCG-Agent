
def _hash_computation(hash_obj, module, ignore_callbacks: IgnoreCallbacks):
  if config.compilation_cache_include_metadata_in_key.value:
    canonical_ir = _serialize_ir(module, ignore_callbacks)
  else:
    canonical_ir = _canonicalize_ir(module, ignore_callbacks)
  hash_obj.update(canonical_ir)

