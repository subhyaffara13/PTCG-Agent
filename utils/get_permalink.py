from typing import Any

def get_permalink(
    *,
    url: str,
    template_params: dict[str, Any] | tuple[tuple[str, Any, Any], ...],
) -> str:
  """Get the permalink for the current colab.

  Args:
    url: The base URL.
    template_params: A dict of name to value. Can also be a list of (name,
      value, default) tuples, in which case only the value != default are added
      (to make the url shorter).

  Returns:
    The permalink.
  """

  # TODO(epot): If url is missing, should auto-extract it from the colab URL.
  if url.startswith('go/'):
    url = f'http://{url}'

  # Normalize the template params to a dict.
  if not isinstance(template_params, dict):
    template_params = {
        name: value
        for name, value, default in template_params
        if value != default  # Only add params which are different from default
    }

  template_params = json_std.dumps(template_params)
  template_params = urllib.parse.quote(template_params)
  return f'{url}#templateParams={template_params}'

