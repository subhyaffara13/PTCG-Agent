
def _fix_request_current_app(app: "Application") -> Middleware:
    @middleware
    async def impl(request: Request, handler: Handler) -> StreamResponse:
        match_info = request.match_info
        prev = match_info.current_app
        match_info.current_app = app
        try:
            return await handler(request)
        finally:
            match_info.current_app = prev

    return impl

