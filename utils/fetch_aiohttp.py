
def fetch_aiohttp(urls: list[str], timeout: float) -> list[Response]:
    # late import for optional dependency
    # pyrefly: ignore [missing-import]
    import aiohttp

    async def fetch(session: aiohttp.ClientSession, url: str) -> Response:
        try:
            async with session.post(url) as resp:
                text = await resp.text()
                return Response(resp.status, text)
        except asyncio.TimeoutError as e:
            return Response(408, f"TimeoutError: {e}")
        except aiohttp.ClientError as e:
            return Response(503, f"{type(e).__name__}: {e}")
        except Exception as e:
            return Response(502, f"{type(e).__name__}: {e}")

    async def gather(urls: list[str]) -> list[Response]:
        client_timeout = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=client_timeout) as session:
            return list(await asyncio.gather(*[fetch(session, url) for url in urls]))

    return asyncio.run(gather(urls))

