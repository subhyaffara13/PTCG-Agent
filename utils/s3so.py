
def s3so(moto_server):
    return {
        "client_kwargs": {
            "endpoint_url": moto_server,
        }
    }

