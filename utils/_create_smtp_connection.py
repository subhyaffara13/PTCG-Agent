
def _create_smtp_connection(smtp_host: str, smtp_port: int) -> smtplib.SMTP:
    if _should_use_smtp_ssl(smtp_port=smtp_port):
        return smtplib.SMTP_SSL(
            host=smtp_host, port=smtp_port, context=ssl.create_default_context()
        )
    return smtplib.SMTP(host=smtp_host, port=smtp_port)

