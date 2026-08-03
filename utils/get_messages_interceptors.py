from typing import List

def get_messages_interceptors() -> List[MessagesInterceptor]:
    """Return the list of active MessagesInterceptors.

    Order matters: interceptors are tried in list order; the first one whose
    ``can_handle()`` returns True wins.
    """
    return _interceptors

