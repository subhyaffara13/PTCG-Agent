
def init_no_clipboard():
    class ClipboardUnavailable:
        def __call__(self, *args, **kwargs):
            raise PyperclipException(EXCEPT_MSG)

        def __bool__(self) -> bool:
            return False

    return ClipboardUnavailable(), ClipboardUnavailable()

