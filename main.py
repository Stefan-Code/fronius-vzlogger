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
    print('Usage: {scriptname} <fronius_ip> <vzlogger_ip> <vzlogger_uuid>'.format(sys.argv[0]))
# Loop forever

update_rate = 20  # seconds
bucket = TokenBucket(10, 1/120)
while True:
    try:
        power = get_power(fronius_ip)
    except InverterException:
        power = 0 # Inverter not available
    try:
        log_power(power)
    except Exception as e:
        print('exception occured:', e)
        if bucket.consume(1, block=False):
            pass
        else:
            print('too many exceptions, aborting')
            raise e
