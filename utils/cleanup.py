from __future__ import annotations
import gc
import threading
import sys
from typing import Callable, List
import torch

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from factory.orchestration_process import Config
# Lazy imports are performed within functions to avoid circular imports.

def cleanup_processes(processes: List[tuple]):
    """Terminate and clean up subprocesses.

    Args:
        processes: Iterable of (process, file) tuples where ``process`` is a
            ``subprocess.Popen`` object and ``file`` is an optional file handle.
    """
    from factory.orchestration_process import logger
    logger.info("Cleaning up sub‑tasks...")
    # First, ask all processes to terminate.
    for p, f in processes:
        if p is not None:
            try:
                p.terminate()
            except Exception:
                pass
    # Then wait for them, falling back to kill if needed, and close files.
    for p, f in processes:
        if p is None:
            continue
        try:
            p.wait(timeout=2)
        except BaseException:
            try:
                p.kill()
            except Exception:
                pass
        if f is not None:
            try:
                f.close()
            except Exception:
                pass

def cleanup_device(device: str, gc_collect: bool = False):
    """Clear device cache and optionally run a full GC.

    Args:
        device: Identifier of the device (e.g., ``"cpu"`` or ``"cuda"``).
        gc_collect: If ``True``, run ``gc.collect()`` before clearing the cache.
    """
    if gc_collect:
        gc.collect()
    from factory.orchestration_process import backend_empty_cache
    backend_empty_cache(device)
    torch.compiler.reset()

def cleanup_config(*, config: Config, prev_hook: Callable[[threading.ExceptHookArgs], object]):
    """Restore the original threading exception hook and clean up the config stash.

    This mirrors the original overload that dealt with thread‑exception handling.
    """
    from factory.orchestration_process import collect_thread_exception, thread_exceptions
    try:
        try:
            collect_thread_exception(config)
        finally:
            threading.excepthook = prev_hook
    finally:
        del config.stash[thread_exceptions]

def cleanup_config_unraisable(*, config: Config, prev_hook: Callable[[sys.UnraisableHookArgs], object]):
    """Handle unraisable exceptions and perform a forced GC pass.

    The number of GC passes depends on the interpreter (5 for PyPy, 1 for CPython).
    """
    from factory.orchestration_process import gc_collect_harder, gc_collect_iterations_key, collect_unraisable, unraisable_exceptions
    _default = 5 if sys.implementation.name == "pypy" else 1
    iterations = config.stash.get(gc_collect_iterations_key, _default)
    try:
        try:
            gc_collect_harder(iterations)
            collect_unraisable(config)
        finally:
            sys.unraisablehook = prev_hook
    finally:
        del config.stash[unraisable_exceptions]

def cleanup_env(env):
    """Remove an environment entry from the global ``m_envs`` dict.

    Args:
        env: An environment object that has a ``configuration.id`` attribute.
    """
    import factory.orchestration_process as _op
    del _op.m_envs[env.configuration.id]
