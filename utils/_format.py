import json
from typing import Any

def _format(
    fields_str: list[str],
    indent: int,
    width: int,
    curr_indent: int,
    start: str,
    end: str,
) -> str:
    delimiter, curr_indent_str = "", ""
    # if it exceed the max width then we place one element per line
    if len(repr(fields_str)) >= width:
        delimiter = "\n"
        curr_indent_str = " " * curr_indent

    indent_str = " " * indent
    body = f", {delimiter}{curr_indent_str}".join(fields_str)
    return f"{start}{indent_str}{body}{end}"


def _format(
    error_type: type[_HfHubHTTPErrorT], custom_message: str, response: httpx.Response, **attrs: Any
) -> _HfHubHTTPErrorT:
    server_errors = []

    # Retrieve server error from header
    from_headers = response.headers.get("X-Error-Message")
    if from_headers is not None:
        server_errors.append(from_headers)

    # Retrieve server error from body
    try:
        # Case errors are returned in a JSON format
        try:
            data = response.json()
        except httpx.ResponseNotRead:
            try:
                response.read()  # In case of streaming response, we need to read the response first
                data = response.json()
            except RuntimeError:
                # In case of async streaming response, we can't read the stream here.
                # In practice if user is using the default async client from `get_async_client`, the stream will have
                # already been read in the async event hook `async_hf_response_event_hook`.
                #
                # Here, we are skipping reading the response to avoid RuntimeError but it happens only if async + stream + used httpx.AsyncClient directly.
                data = {}

        error = data.get("error")
        error_description = data.get("error_description")
        if error is not None:
            if isinstance(error, list):
                # Case {'error': ['my error 1', 'my error 2']}
                server_errors.extend(error)
            elif error_description is not None:
                # OAuth-style case {'error': 'invalid_grant', 'error_description': 'my description'}
                server_errors.append(f"{error}: {error_description}")
            else:
                # Case {'error': 'my error'}
                server_errors.append(error)
        elif error_description is not None:
            # Case {'error_description': 'my description'} (no 'error' field)
            server_errors.append(error_description)

        errors = data.get("errors")
        if errors is not None:
            # Case {'errors': [{'message': 'my error 1'}, {'message': 'my error 2'}]}
            for error in errors:
                if "message" in error:
                    server_errors.append(error["message"])

    except json.JSONDecodeError:
        # If content is not JSON and not HTML, append the text
        content_type = response.headers.get("Content-Type", "")
        if response.text and "html" not in content_type.lower():
            server_errors.append(response.text)

    # Strip all server messages
    server_errors = [str(line).strip() for line in server_errors if str(line).strip()]

    # Deduplicate server messages (keep order)
    # taken from https://stackoverflow.com/a/17016257
    server_errors = list(dict.fromkeys(server_errors))

    # Format server error
    server_message = "\n".join(server_errors)

    # Add server error to custom message
    final_error_message = custom_message
    if server_message and server_message.lower() not in custom_message.lower():
        if "\n\n" in custom_message:
            final_error_message += "\n" + server_message
        else:
            final_error_message += "\n\n" + server_message

    # Prepare Request ID message
    request_id = ""
    request_id_message = ""
    for header, label in (
        (X_REQUEST_ID, "Request ID"),
        (X_AMZN_TRACE_ID, "Amzn Trace ID"),
        (X_AMZ_CF_ID, "Amz CF ID"),
    ):
        value = response.headers.get(header)
        if value:
            request_id = str(value)
            request_id_message = f" ({label}: {value})"
            break

    # Add Request ID
    if request_id and request_id.lower() not in final_error_message.lower():
        if "\n" in final_error_message:
            newline_index = final_error_message.index("\n")
            final_error_message = (
                final_error_message[:newline_index] + request_id_message + final_error_message[newline_index:]
            )
        else:
            final_error_message += request_id_message

    # Return
    err = error_type(final_error_message.strip(), response=response, server_message=server_message or None)
    for k, v in attrs.items():
        setattr(err, k, v)
    return err

