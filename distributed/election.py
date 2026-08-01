import socket
import time
import json
import threading

ELECTION_PORT = 9873

from utils.get_local_ip import get_local_ip

from utils.run_election import run_election
