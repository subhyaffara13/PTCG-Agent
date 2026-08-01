
def register_module_custom_calls(module):
  if hasattr(module, "registrations"):
    for platform, targets in module.registrations().items():
      for name, value, api_version in targets:
        ffi.register_ffi_target(
            name, value, platform=platform, api_version=api_version
        )
  if hasattr(module, "batch_partitionable_targets"):
    for name in module.batch_partitionable_targets():
      ffi.register_ffi_target_as_batch_partitionable(name)

