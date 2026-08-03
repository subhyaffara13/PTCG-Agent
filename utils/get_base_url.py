from typing import Any, Dict, Optional

def get_base_url(spec: Dict[str, Any], spec_path: Optional[str] = None) -> str:
    """Extract base URL from OpenAPI spec."""
    # OpenAPI 3.x
    if "servers" in spec and spec["servers"]:
        server_url = spec["servers"][0]["url"]

        # If the server URL is relative (starts with /), derive base from spec_path
        if server_url.startswith("/") and spec_path:
            if spec_path.startswith("http://") or spec_path.startswith("https://"):
                # Extract base URL from spec_path (e.g., https://petstore3.swagger.io/api/v3/openapi.json)
                # Combine domain with the relative server URL
                from urllib.parse import urlparse

                parsed = urlparse(spec_path)
                base_domain = f"{parsed.scheme}://{parsed.netloc}"
                full_base_url = base_domain + server_url
                verbose_logger.info(
                    f"OpenAPI spec has relative server URL '{server_url}'. "
                    f"Deriving base from spec_path: {full_base_url}"
                )
                return full_base_url

        return server_url
    # OpenAPI 2.x (Swagger)
    elif "host" in spec:
        scheme = spec.get("schemes", ["https"])[0]
        base_path = spec.get("basePath", "")
        return f"{scheme}://{spec['host']}{base_path}"

    # Fallback: derive base URL from spec_path if it's a URL
    if spec_path and (
        spec_path.startswith("http://") or spec_path.startswith("https://")
    ):
        for suffix in [
            "/openapi.json",
            "/openapi.yaml",
            "/swagger.json",
            "/swagger.yaml",
        ]:
            if spec_path.endswith(suffix):
                base_url = spec_path[: -len(suffix)]
                verbose_logger.info(
                    f"No server info in OpenAPI spec. Using derived base URL: {base_url}"
                )
                return base_url

        if spec_path.split("/")[-1].endswith((".json", ".yaml", ".yml")):
            base_url = "/".join(spec_path.split("/")[:-1])
            verbose_logger.info(
                f"No server info in OpenAPI spec. Using derived base URL: {base_url}"
            )
            return base_url

    return ""

