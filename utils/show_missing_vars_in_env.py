
def show_missing_vars_in_env():
    from fastapi.responses import HTMLResponse

    from litellm.proxy.proxy_server import master_key, prisma_client

    if prisma_client is None and master_key is None:
        return HTMLResponse(
            content=missing_keys_form(
                missing_key_names="DATABASE_URL, LITELLM_MASTER_KEY"
            ),
            status_code=200,
        )
    if prisma_client is None:
        return HTMLResponse(
            content=missing_keys_form(missing_key_names="DATABASE_URL"), status_code=200
        )

    if master_key is None:
        return HTMLResponse(
            content=missing_keys_form(missing_key_names="LITELLM_MASTER_KEY"),
            status_code=200,
        )
    return None

