
def fetch_thread_pool(urls: list[str], timeout: float) -> list[Response]:
    # late import for optional dependency
    import requests

    max_workers = 20

    def get(url: str) -> Response:
        try:
            resp = requests.post(url, timeout=timeout)
            return Response(resp.status_code, resp.text)
        except requests.exceptions.Timeout as e:
            return Response(408, f"Timeout: {e}")
        except requests.exceptions.ConnectionError as e:
            return Response(503, f"ConnectionError: {e}")
        except Exception as e:
            return Response(502, f"{type(e).__name__}: {e}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        resps = list(executor.map(get, urls))

    return resps

