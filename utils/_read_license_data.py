
def _read_license_data() -> Optional[Dict[str, Any]]:
    from litellm.proxy.proxy_server import _license_check, premium_user_data

    license_data: Optional[EnterpriseLicenseData] = (
        premium_user_data or _license_check.airgapped_license_data
    )

    if (
        license_data is None
        and getattr(_license_check, "license_str", None)
        and getattr(_license_check, "public_key", None)
    ):
        try:
            verification_result = _license_check.verify_license_without_api_request(
                public_key=_license_check.public_key,
                license_key=_license_check.license_str,
            )
            if verification_result is True:
                license_data = _license_check.airgapped_license_data
        except Exception:
            pass

    if license_data is None:
        return None
    return cast(Dict[str, Any], license_data)

