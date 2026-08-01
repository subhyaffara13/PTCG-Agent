
def in_string_annotation(func):
    @functools.wraps(func)
    def in_annotation_func(self, *args, **kwargs):
        with self._enter_annotation(AnnotationState.STRING):
            return func(self, *args, **kwargs)
    return in_annotation_func

