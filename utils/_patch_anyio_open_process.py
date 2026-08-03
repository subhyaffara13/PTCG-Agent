import sys

def _patch_anyio_open_process():
    """
    Patch anyio.open_process to allow detached processes on Windows and Unix-like systems.

    This is necessary to prevent the MCP client from being interrupted by Ctrl+C when running in the CLI.
    """
    import subprocess

    import anyio

    if getattr(anyio, "_tiny_agents_patched", False):
        return
    anyio._tiny_agents_patched = True  # ty: ignore[invalid-assignment]

    original_open_process = anyio.open_process

    if sys.platform == "win32":
        # On Windows, we need to set the creation flags to create a new process group

        async def open_process_in_new_group(*args, **kwargs):
            """
            Wrapper for open_process to handle Windows-specific process creation flags.
            """
            # Ensure we pass the creation flags for Windows
            kwargs.setdefault("creationflags", subprocess.CREATE_NEW_PROCESS_GROUP)
            return await original_open_process(*args, **kwargs)

        anyio.open_process = open_process_in_new_group  # ty: ignore[invalid-assignment]
    else:
        # For Unix-like systems, we can use setsid to create a new session
        async def open_process_in_new_group(*args, **kwargs):
            """
            Wrapper for open_process to handle Unix-like systems with start_new_session=True.
            """
            kwargs.setdefault("start_new_session", True)
            return await original_open_process(*args, **kwargs)

        anyio.open_process = open_process_in_new_group  # ty: ignore[invalid-assignment]

