
def management_endpoint_wrapper(func):
    """
    This wrapper does the following:

    1. Log I/O, Exceptions to OTEL
    2. Create an Audit log for success calls
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = datetime.now()
        try:
            result = await func(*args, **kwargs)
            end_time = datetime.now()
            try:
                user_api_key_dict: UserAPIKeyAuth = (
                    kwargs.get("user_api_key_dict") or UserAPIKeyAuth()
                )

                await send_management_endpoint_alert(
                    request_kwargs=kwargs,
                    user_api_key_dict=user_api_key_dict,
                    function_name=func.__name__,
                )
                parent_otel_span = getattr(user_api_key_dict, "parent_otel_span", None)
                if parent_otel_span is not None:
                    await _emit_management_endpoint_otel_span(
                        func=func,
                        kwargs=kwargs,
                        parent_otel_span=parent_otel_span,
                        start_time=start_time,
                        end_time=end_time,
                        result=result,
                    )

                # Delete updated/deleted info from cache
                _delete_api_key_from_cache(kwargs=kwargs)
                _delete_user_id_from_cache(kwargs=kwargs)
                _delete_team_id_from_cache(kwargs=kwargs)
                _delete_customer_id_from_cache(kwargs=kwargs)
            except Exception as e:
                # Non-Blocking Exception
                verbose_logger.debug("Error in management endpoint wrapper: %s", str(e))
                pass

            return result
        except Exception as e:
            end_time = datetime.now()

            user_api_key_dict: UserAPIKeyAuth = (
                kwargs.get("user_api_key_dict") or UserAPIKeyAuth()
            )
            parent_otel_span = getattr(user_api_key_dict, "parent_otel_span", None)
            if parent_otel_span is not None:
                try:
                    await _emit_management_endpoint_otel_span(
                        func=func,
                        kwargs=kwargs,
                        parent_otel_span=parent_otel_span,
                        start_time=start_time,
                        end_time=end_time,
                        exception=e,
                    )
                except Exception as otel_exc:
                    # Non-Blocking Exception - never let OTEL failures swallow
                    # the original management-endpoint exception.
                    verbose_logger.debug(
                        "Error emitting OTEL span in management endpoint wrapper failure path: %s",
                        str(otel_exc),
                    )

            raise e

    return wrapper

