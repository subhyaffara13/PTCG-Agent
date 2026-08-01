
def finalize(path: path_types.PathLike) -> None:
  """Finalizes a partially-saved checkpoint, making it permanent and readable.

  This function commits all changes made during a partial save session,
  concluding the transaction. It should be called once after all desired
  :py:func:`.save` operations are complete.

  The finalization process is atomic. It renames the temporary, versioned
  partial save directory to the final target `path`, making the updated
  checkpoint "live".

  IMPORTANT: Until `finalize` is called, the checkpoint at the target `path`
  is not created or modified. All changes are buffered in a temporary location.
  This function is what makes those changes permanent.


  ### Example::
    path = '/path/to/my/checkpoint'

    # These calls write to a temporary, versioned directory, not the final path.
    ocp.partial.save(path, {'step': 1})
    ocp.partial.save_checkpointables(path, {'metrics': ...})

    # This call performs the atomic rename, making the checkpoint available at
    # '/path/to/my/checkpoint'.
    ocp.partial.finalize(path)

  Args:
    path: The final, target path of the checkpoint to be finalized. This should
      be the same path that was passed to :py:func:`~.save` calls.

  Raises:
    FileExistsError: If a finalized checkpoint already exists at `path`. To
      overwrite, it must be deleted first.
    FileNotFoundError: If no partial save session is found for the given `path`.
      This can happen if :py:func:`.save` was not called first.
  """
  context = context_lib.get_context()
  path = context.file_options.path_class(path)
  if partial_path_lib.is_partial_save_path(path):
    final_path = partial_path_lib.remove_partial_save_suffix(path)
    partial_path = path
  else:
    final_path = path
    partial_path = partial_path_lib.add_partial_save_suffix(path)

  async def _finalize_impl():
    await multihost.sync_global_processes(
        multihost.unique_barrier_key(
            'OcpPartialSaving:finalize_path_existence_start',
            prefix=context.multiprocessing_options.barrier_sync_key_prefix,
        ),
        operation_id=synchronization.get_operation_id(),
        processes=context.multiprocessing_options.active_processes,
    )
    if await async_path.exists(final_path):
      raise FileExistsError(
          f'Finalized checkpoint already exists at {final_path}.'
      )
    elif not await async_path.exists(partial_path):
      raise FileNotFoundError(
          f'Partial save path {partial_path} does not exist.'
      )

    await multihost.sync_global_processes(
        multihost.unique_barrier_key(
            'OcpPartialSaving:finalize_path_rename_start',
            prefix=context.multiprocessing_options.barrier_sync_key_prefix,
        ),
        operation_id=synchronization.get_operation_id(),
        processes=context.multiprocessing_options.active_processes,
    )

    finalize_failed = False
    finalize_error = None
    if multihost.is_primary_host(context.multiprocessing_options.primary_host):
      try:
        await _merge_all(partial_path)
        await async_path.rename(partial_path, final_path)
      except (ValueError, OSError) as e:
        finalize_failed = True
        finalize_error = e

    finalize_failed = multihost.broadcast_one_to_all(
        finalize_failed,
        is_source=multihost.is_primary_host(
            context.multiprocessing_options.primary_host
        ),
    )

    await multihost.sync_global_processes(
        multihost.unique_barrier_key(
            'OcpPartialSaving:finalize_rename_complete',
            prefix=context.multiprocessing_options.barrier_sync_key_prefix,
        ),
        operation_id=synchronization.get_operation_id(),
        processes=context.multiprocessing_options.active_processes,
    )

    if finalize_failed:
      raise finalize_error or OSError('Partial checkpoint finalization failed.')

  asyncio_utils.run_sync(_finalize_impl())

