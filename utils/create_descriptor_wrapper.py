
def create_descriptor_wrapper(descriptor: Descriptor):
  """Creates a descriptor wrapper that calls a get_fn on the descriptor."""

  class _DescriptorWrapper(DescriptorWrapper):
    """A descriptor that can wrap any descriptor."""

    if hasattr(descriptor, '__isabstractmethod__'):
      __isabstractmethod__ = descriptor.__isabstractmethod__

    def __init__(self, wrapped: Descriptor):
      self.wrapped = wrapped

    # conditionally define descriptor methods
    if hasattr(descriptor, '__get__'):

      def __get__(self, *args, **kwargs):
        # here we will catch internal AttributeError and re-raise it as a
        # more informative and correct error message.
        try:
          return self.wrapped.__get__(*args, **kwargs)
        except AttributeError as e:
          raise errors.DescriptorAttributeError() from e

    if hasattr(descriptor, '__set__'):

      def __set__(self, *args, **kwargs):
        return self.wrapped.__set__(*args, **kwargs)

    if hasattr(descriptor, '__delete__'):

      def __delete__(self, *args, **kwargs):
        return self.wrapped.__delete__(*args, **kwargs)

    if hasattr(descriptor, '__set_name__'):

      def __set_name__(self, *args, **kwargs):
        self.wrapped.__set_name__(*args, **kwargs)

    def __getattr__(self, name):
      if 'wrapped' not in vars(self):
        raise AttributeError()
      return getattr(self.wrapped, name)

  return _DescriptorWrapper(descriptor)

