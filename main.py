#!/usr/bin/env python3

import time
import sys

from vzlog import log_power
from fronius import get_power
from fronius import InverterException
from token_bucket import TokenBucket

try:
    fronius_ip = sys.argv[1]
    vzlog_ip = sys.argv[2]
    vzlog_uuid = sys.argv[3]
except:
    print('Usage: {} <fronius_ip> <vzlogger_ip> <vzlogger_uuid>'.format(sys.argv[0]))
    sys.exit(1)
# Loop forever

update_rate = 20  # seconds
bucket = TokenBucket(10, 1/120)
fronius_consecutive_errors = 0
fronius_consecutive_threshold = 3

def log_power_handled(power):
    if power is not None:
        try:
            log_power(power, vzlog_uuid, address=vzlog_ip)
            print('logged {} Watts'.format(power))
        except Exception as e:
            print('exception occured:', e)
            if bucket.consume(1, block=False):
                pass
            else:
                print('too many exceptions, aborting')
                raise e

while True:
    try:
        power = get_power(fronius_ip)
    except InverterException as e:
        fronius_consecutive_errors += 1
        power = None
        print('Inverter not reachable (#{}): '.format(fronius_consecutive_errors), e)
        if fronius_consecutive_errors == fronius_consecutive_threshold:
            # seems like the inverter is really down, log 0 watts ONCE:
            print("marking inverter as unreachable!")
            log_power_handled(0)
    else:
        if fronius_consecutive_errors >= fronius_consecutive_threshold:
            log_power_handled(0)
        time.sleep(1)
        log_power_handled(power)
        fronius_consecutive_errors = 0
    time.sleep(update_rate)
