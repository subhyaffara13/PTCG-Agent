
def default_response_schema_prompt(response_schema: dict) -> str:
    """
    Used if provider/model doesn't support 'response_schema' param.

    This is the default prompt. Allow user to override this with a custom_prompt.
    """
    prompt_str = """Use this JSON schema: 
    ```json 
    {}
    ```""".format(response_schema)
    return prompt_str

