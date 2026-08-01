
def _consume(iterator):
    "Consume the iterator entirely."
    # Feed the entire iterator into a zero-length deque.
    deque(iterator, maxlen=0)

