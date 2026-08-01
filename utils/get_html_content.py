
def get_html_content(id_: str) -> str:
  """Returns the inner content of the block id.

  Is called the first time a block is expanded.

  Args:
    id_: Id of the block to load

  Returns:
    The html to add.
  """
  try:
    node = nodes.Node.from_id(id_)
    return node.inner_html
  except Exception as e:  # pylint: disable=broad-except
    epy.reraise(
        e,
        prefix=(
            '`ecolab.inspect` internal error. Please report an issue'
            '.\n'
        ),
    )

