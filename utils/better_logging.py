
def better_logging():
  """Improve Python logging when running locally.

  * Display Python logs by default (even when user forgot `--logtostderr`),
    without being polluted by hundreds of C++ logs.
  * Cleaner minimal log format (e.g. `I 15:04:05 [main.py:24]:`)
  * Avoid visual artifacts between TQDM & `logging`
  * Clickable hyperlinks redirecting to code search (require terminal support)

  Usage:

  ```python
  if __name__ == '__main__':
    eapp.better_logging()
    app.run(main)
  ```

  Note this has only effect when user run locally and without `--logtostderr`.
  """
  app.call_after_init(_better_logging)

