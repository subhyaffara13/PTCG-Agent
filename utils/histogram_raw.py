
def histogram_raw(name, min, max, num, sum, sum_squares, bucket_limits, bucket_counts):
    # pylint: disable=line-too-long
    """Output a `Summary` protocol buffer with a histogram.

    The generated
    [`Summary`](https://www.tensorflow.org/code/tensorflow/core/framework/summary.proto)
    has one summary value containing a histogram for `values`.
    Args:
      name: A name for the generated node. Will also serve as a series name in
        TensorBoard.
      min: A float or int min value
      max: A float or int max value
      num: Int number of values
      sum: Float or int sum of all values
      sum_squares: Float or int sum of squares for all values
      bucket_limits: A numeric `Tensor` with upper value per bucket
      bucket_counts: A numeric `Tensor` with number of values per bucket
    Returns:
      A scalar `Tensor` of type `string`. The serialized `Summary` protocol
      buffer.
    """
    hist = HistogramProto(
        min=min,
        max=max,
        num=num,
        sum=sum,
        sum_squares=sum_squares,
        bucket_limit=bucket_limits,
        bucket=bucket_counts,
    )
    return Summary(value=[Summary.Value(tag=name, histo=hist)])

