
def _make_handler(
        url: str,
        method: str,
        timeout: Optional[float],
        headers: Sequence[Tuple[str, str]],
        data: bytes,
        base_handler: Union[BaseHandler, type],
) -> Callable[[], None]:
    def handle() -> None:
        request = Request(url, data=data)
        request.get_method = lambda: method  # type: ignore
        for k, v in headers:
            request.add_header(k, v)
        resp = build_opener(base_handler).open(request, timeout=timeout)
        if resp.code >= 400:
            raise OSError(f"error talking to pushgateway: {resp.code} {resp.msg}")

    return handle

