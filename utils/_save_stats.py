
def _save_stats(profile_file: PathLib) -> None:
    """Save current stats directly to file."""
    with _profile_lock:
        if _profiler is None:
            return
        try:
            # Disable profiler temporarily to dump stats
            _profiler.disable()
            _profiler.dump_stats(str(profile_file))
            # Re-enable profiler to continue profiling
            _profiler.enable()
            verbose_proxy_logger.debug(f"Profiling stats saved to {profile_file}")
        except Exception as e:
            verbose_proxy_logger.error(f"Error saving profiling stats: {e}")
            # Make sure profiler is re-enabled even if there's an error
            try:
                _profiler.enable()
            except Exception:
                pass

