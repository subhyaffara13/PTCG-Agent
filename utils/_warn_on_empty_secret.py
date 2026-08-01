
def _warn_on_empty_secret(webhook_secret: str | None) -> None:
    if webhook_secret is None:
        print("Webhook secret is not defined. This means your webhook endpoints will be open to everyone.")
        print(
            "To add a secret, set `WEBHOOK_SECRET` as environment variable or pass it at initialization: "
            "\n\t`app = WebhooksServer(webhook_secret='my_secret', ...)`"
        )
        print(
            "For more details about webhook secrets, please refer to"
            " https://huggingface.co/docs/hub/webhooks#webhook-secret."
        )
    else:
        print("Webhook secret is correctly defined.")

