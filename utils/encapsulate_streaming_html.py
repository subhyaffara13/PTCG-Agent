import uuid

def encapsulate_streaming_html(
    inner_iterator: Iterable[str],
    *,
    compress: bool = True,
    stealable: bool = False,
) -> Iterator[HTMLOutputSegment]:
  """Encapsulates a sequence of inner HTML blobs into robust iframe updates.

  This function accepts an iterator of HTML blobs that should each run in the
  same iframe, and transforms them into another iterator of HTML blobs that
  can be inserted directly into a notebook environment. The first output will
  set up the iframe, and all later updates will insert content into that
  original iframe. Optionally, the final output will be a "stealer" that will
  move the iframe into itself, ensuring that the iframe is associated with the
  correct "result" cell in IPython notebook systems that show Out[...] markers.
  Updates will be duplication-safe, in the sense that repeating the same
  sequence of outputs in a single HTML page will produce multiple copies of the
  iframe, each with the same contents, and the code in the inner iterator will
  only be executed once in each iframe.

  Args:
    inner_iterator: A nonempty iterator of HTML blobs to encapsulate.
    compress: Whether to compress the HTML blobs.
    stealable: Whether to include a final "stealer" blob that will move the
      iframe into itself.

  Yields:
    HTML output segments that can be displayed in a notebook environment or
    saved.
  """
  inner_iterator = iter(inner_iterator)

  stream = io.StringIO()
  # Build the initial iframe, and assign it a unique ID.
  # Note: This is unique in the Python program, but if the output is repeated
  # multiple times in the notebook output, we may have multiple iframes with
  # the same ID.
  unique_id_class = f"treescope_out_{uuid.uuid4().hex}"

  outer_content = _prep_html_js_and_strip_comments(CONTAINER_TEMPLATE).replace(
      "{__REPLACE_ME_WITH_CONTAINER_ID_CLASS__}", unique_id_class
  )
  stream.write(outer_content)

  for i, step_content in enumerate(inner_iterator):
    if compress:
      # Compress the input string. We use ZLIB, which is natively supported by
      # modern browsers.
      compressed = zlib.compress(
          step_content.encode("utf-8"), zlib.Z_BEST_COMPRESSION
      )
      # Serialize it as base64.
      serialized = base64.b64encode(compressed).decode("ascii")
      # Embed it.
      step_content = (
          _prep_html_js_and_strip_comments(COMPRESSED_STEP_TEMPLATE)
          .replace("{__REPLACE_ME_WITH_CONTAINER_ID_CLASS__}", unique_id_class)
          .replace("{__REPLACE_ME_WITH_STEP__}", str(i))
          .replace("{__REPLACE_ME_WITH_COMPRESSED_CONTENT_HTML__}", serialized)
      )
    else:
      step_content = (
          _prep_html_js_and_strip_comments(STEP_TEMPLATE)
          .replace("{__REPLACE_ME_WITH_CONTAINER_ID_CLASS__}", unique_id_class)
          .replace("{__REPLACE_ME_WITH_STEP__}", str(i))
          .replace("{__REPLACE_ME_WITH_CONTENT_HTML__}", step_content)
      )
    stream.write(step_content)
    if i == 0:
      segment_type = SegmentType.CONTAINER
    else:
      segment_type = SegmentType.CONTAINER_UPDATE
    yield HTMLOutputSegment(
        html_src=stream.getvalue(), segment_type=segment_type
    )
    stream = io.StringIO()

  if stealable:
    stealer_content = _prep_html_js_and_strip_comments(
        STEALER_TEMPLATE
    ).replace("{__REPLACE_ME_WITH_CONTAINER_ID_CLASS__}", unique_id_class)
    yield HTMLOutputSegment(
        html_src=stealer_content,
        segment_type=SegmentType.FINAL_OUTPUT_STEALER,
    )

