
def init_policies_sync(
    policies_config: Dict[str, Any],
    policy_attachments_config: Optional[List[Dict[str, Any]]] = None,
    fail_on_error: bool = True,
) -> None:
    """
    Synchronous version of init_policies (without DB validation).

    Use this when async is not available or DB validation is not needed.

    Args:
        policies_config: Dictionary mapping policy names to policy definitions
        policy_attachments_config: Optional list of policy attachment configurations
        fail_on_error: If True, raise exception on validation errors
    """
    import asyncio

    # Run the async function without DB validation
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(
        init_policies(
            policies_config=policies_config,
            policy_attachments_config=policy_attachments_config,
            prisma_client=None,
            validate_db=False,
            fail_on_error=fail_on_error,
        )
    )

