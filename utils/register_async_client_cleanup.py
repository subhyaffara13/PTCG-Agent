
def register_async_client_cleanup():
    """
    Register the async client cleanup function to run at exit.

    This ensures that all async HTTP clients are properly closed when the program exits.
    """
    import atexit

    def cleanup_wrapper():
        """
        Cleanup wrapper that creates a fresh event loop for atexit cleanup.

        At exit time, the main event loop is often already closed. Creating a new
        event loop ensures cleanup runs successfully (fixes issue #12443).
        """
        try:
            # Always create a fresh event loop at exit time
            # Don't use get_event_loop() - it may be closed or unavailable
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(close_litellm_async_clients())
            finally:
                # Clean up the loop we created
                loop.close()
        except Exception:
            # Silently ignore errors during cleanup to avoid exit handler failures
            pass

    atexit.register(cleanup_wrapper)

