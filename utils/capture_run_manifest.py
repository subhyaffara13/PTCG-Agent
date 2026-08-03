import os

def capture_run_manifest() -> RunManifest:
  """Captures every reproducibility-relevant fact about the current process."""
  git_sha = _safe_check_output(["git", "rev-parse", "HEAD"]) or "unknown"
  git_status = _safe_check_output(["git", "status", "--porcelain"])
  git_dirty = bool(git_status.strip())

  pc, pi, dc, kind = _capture_topology()

  return RunManifest(
      captured_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      hostname=socket.gethostname(),
      git_sha=git_sha,
      git_dirty=git_dirty,
      jax_version=_safe_module_version("jax"),
      orbax_version=_safe_module_version("orbax.checkpoint"),
      tensorstore_version=_safe_module_version("tensorstore"),
      jax_process_count=pc,
      jax_process_index=pi,
      jax_device_count=dc,
      jax_device_kind=kind,
      xla_flags=os.environ.get("XLA_FLAGS", ""),
      libtpu_init_args=os.environ.get("LIBTPU_INIT_ARGS", ""),
  )

