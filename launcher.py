import os
import subprocess
import signal
from config import *
import time

wholetime = bet_time * 1.5

while True:
    proc = subprocess.Popen(['python3', 'main.py'])
    time.sleep(wholetime + 10)
    os.kill(proc.pid, signal.SIGTERM)
    time.sleep(0.5)
    os.kill(proc.pid, signal.SIGTERM)
