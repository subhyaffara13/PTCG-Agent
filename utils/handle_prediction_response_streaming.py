import time

def handle_prediction_response_streaming(
    prediction_url, api_token, print_verbose, headers: dict, http_client: HTTPHandler
):
    previous_output = ""
    output_string = ""

    status = ""
    while True and (status not in ["succeeded", "failed", "canceled"]):
        time.sleep(
            REPLICATE_POLLING_DELAY_SECONDS
        )  # prevent being rate limited by replicate
        print_verbose(f"replicate: polling endpoint: {prediction_url}")
        response = http_client.get(prediction_url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            status = response_data["status"]
            if "output" in response_data:
                try:
                    output_string = "".join(response_data["output"])
                except Exception:
                    raise ReplicateError(
                        status_code=422,
                        message="Unable to parse response. Got={}".format(
                            response_data["output"]
                        ),
                        headers=response.headers,
                    )
                new_output = output_string[len(previous_output) :]
                print_verbose(f"New chunk: {new_output}")
                yield {"output": new_output, "status": status}
                previous_output = output_string
            status = response_data["status"]
            if status == "failed":
                replicate_error = response_data.get("error", "")
                raise ReplicateError(
                    status_code=400,
                    message=f"Error: {replicate_error}",
                    headers=response.headers,
                )
        else:
            # this can fail temporarily but it does not mean the replicate request failed, replicate request fails when status=="failed"
            print_verbose(
                f"Replicate: Failed to fetch prediction status and output.{response.status_code}{response.text}"
            )

