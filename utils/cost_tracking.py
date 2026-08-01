
def cost_tracking():
    global prisma_client
    if prisma_client is not None:
        litellm.logging_callback_manager.add_litellm_callback(_ProxyDBLogger())
        litellm.logging_callback_manager.add_litellm_async_success_callback(
            _ProxyDBLogger()
        )

