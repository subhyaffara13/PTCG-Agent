from __future__ import annotations
import gc
import threading
import sys
from typing import Callable, List, Any
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
    try:
        from factory.orchestration_process import backend_empty_cache
        backend_empty_cache(device)
    except (ImportError, AttributeError):
        pass
    if hasattr(torch, "compiler") and hasattr(torch.compiler, "reset"):
        torch.compiler.reset()

def cleanup_config(*, config: Any, prev_hook: Callable[[threading.ExceptHookArgs], object]):
    """Restore the original threading exception hook and clean up the config stash."""
    try:
        from factory.orchestration_process import collect_thread_exception, thread_exceptions
        try:
            collect_thread_exception(config)
        finally:
            threading.excepthook = prev_hook
    except (ImportError, AttributeError):
        threading.excepthook = prev_hook

def cleanup_config_unraisable(*, config: Any, prev_hook: Callable[[sys.UnraisableHookArgs], object]):
    """Handle unraisable exceptions and perform a forced GC pass."""
    try:
        from factory.orchestration_process import gc_collect_harder, gc_collect_iterations_key, collect_unraisable, unraisable_exceptions
        _default = 5 if sys.implementation.name == "pypy" else 1
        iterations = getattr(config, "stash", {}).get(gc_collect_iterations_key, _default)
        try:
            gc_collect_harder(iterations)
            collect_unraisable(config)
        finally:
            sys.unraisablehook = prev_hook
    except (ImportError, AttributeError):
        sys.unraisablehook = prev_hook

def cleanup_env(env):
    """Remove an environment entry from the global ``m_envs`` dict."""
    try:
        import factory.orchestration_process as _op
        if hasattr(_op, "m_envs"):
            del _op.m_envs[env.configuration.id]
    except (ImportError, AttributeError, KeyError):
        pass

