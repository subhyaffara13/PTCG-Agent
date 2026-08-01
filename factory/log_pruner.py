import os
import glob
import logging
from typing import List

logger = logging.getLogger("LogPruner")

from utils.prune_logs import prune_logs
