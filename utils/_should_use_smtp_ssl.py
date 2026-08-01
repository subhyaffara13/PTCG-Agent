
def _should_use_smtp_ssl(smtp_port: int) -> bool:
    """
    Port 465 expects an immediate TLS handshake (implicit SSL), so a plain
    smtplib.SMTP connection hangs waiting for an SMTP banner. Use SMTP_SSL
    there, or when SMTP_USE_SSL is explicitly enabled.
    """
    return os.getenv("SMTP_USE_SSL", "False") == "True" or smtp_port == 465

