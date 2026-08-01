
def get_watsonx_iam_url():
    return (
        get_secret_str("WATSONX_IAM_URL") or "https://iam.cloud.ibm.com/identity/token"
    )

