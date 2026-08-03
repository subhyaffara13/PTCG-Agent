import logging
from typing import Any

def _check_templates_match(t0: Any, t1: Any) -> None:
  if t0 != t1:
    logging.warning(
        'Mismatched templates: \nCurrent Template - t0= %s \nOther Template -'
        ' t1= %s ',
        t0,
        t1,
    )
    raise Error('Mismatched templates')

