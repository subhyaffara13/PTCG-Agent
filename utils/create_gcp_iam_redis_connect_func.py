from typing import Callable, Optional

def create_gcp_iam_redis_connect_func(
    service_account: str,
    ssl_ca_certs: Optional[str] = None,
) -> Callable:
    """
    Creates a custom Redis connection function for GCP IAM authentication.

    Args:
        service_account: GCP service account in format 'projects/-/serviceAccounts/name@project.iam.gserviceaccount.com'
        ssl_ca_certs: Path to SSL CA certificate file for secure connections

    Returns:
        A connection function that can be used with Redis clients
    """

    def iam_connect(self):
        """Initialize the connection and authenticate using GCP IAM"""
        from redis.exceptions import (
            AuthenticationError,
            AuthenticationWrongNumberOfArgsError,
        )
        from redis.utils import str_if_bytes

        self._parser.on_connect(self)

        auth_args = (_generate_gcp_iam_access_token(service_account),)
        self.send_command("AUTH", *auth_args, check_health=False)

        try:
            auth_response = self.read_response()
        except AuthenticationWrongNumberOfArgsError:
            # Fallback to password auth if IAM fails
            if hasattr(self, "password") and self.password:
                self.send_command("AUTH", self.password, check_health=False)
                auth_response = self.read_response()
            else:
                raise

        if str_if_bytes(auth_response) != "OK":
            raise AuthenticationError("GCP IAM authentication failed")

    return iam_connect

