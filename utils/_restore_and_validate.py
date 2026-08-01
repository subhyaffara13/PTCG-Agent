
def _restore_and_validate(
    manager: emergency_checkpoint_manager.CheckpointManager,
    metrics: metric_lib.Metrics,
    pytree: Any,
    step: int,
    local_directory: epath.Path,
    is_in_primary_slice: bool,
    is_in_secondary_slice: bool,
    restore_args: Any,
):
  """Restores a checkpoint and validates it."""
  # Wait for save to complete on all hosts.
  with metrics.measure(f"sync_global_processes_{step}"):
    multihost.sync_global_processes(f"save_completed_{step}")


  with metrics.measure(f"reload_first_time_{step}"):
    manager.reload()
  with metrics.measure(f"restore_{step}"):
    restored = manager.restore(
        step,
        args=composite_checkpoint_handler.CompositeArgs(
            state=pytree_checkpoint_handler.PyTreeRestoreArgs(
                restore_args=restore_args
            )
        ),
    )["state"]
  pytree_utils.log_pytree("Local Restored Pytree", restored)
  logging.info("Assert Local Restored Pytree")
  pytree_utils.assert_pytree_equal(pytree, restored)


  with metrics.measure(f"reload_second_time_{step}"):
    manager.reload()


def _restore_and_validate(
    manager: p2p_checkpoint_manager.CheckpointManager,
    metrics: metric_lib.Metrics,
    pytree: Any,
    abstract_pytree: Any,
    step: int,
    restore_args: Any,
    test_name: str = '',
):
  """Restores a checkpoint and validates it."""
  prefix = f'{test_name}_' if test_name else ''
  # Wait for save to complete on all hosts.
  with metrics.measure(f'{prefix}sync_global_processes_{step}'):
    multihost.sync_global_processes(f'{prefix}save_completed_{step}')

  with metrics.measure(f'{prefix}restore_{step}'):
    restored = manager.restore(
        step,
        args=p2p_args_lib.Composite(
            state=pytree_checkpoint_handler.PyTreeRestoreArgs(
                restore_args=restore_args,
                item=abstract_pytree,
            )
        ),
    )['state']
  logging.info('Assert Restored Pytree')
  pytree_utils.assert_pytree_equal(pytree, restored)
  with metrics.measure(f'{prefix}reload_after_restore_{step}'):
    manager.reload()

