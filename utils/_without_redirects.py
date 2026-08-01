
def _without_redirects(options: FinalRequestOptions) -> FinalRequestOptions:
    if options.follow_redirects:
        raise OpenAIError(
            "Bedrock SigV4 authentication does not support automatic redirects. "
            "Send a new request to the redirect target so it can be signed again."
        )
    options.follow_redirects = False
    return options

