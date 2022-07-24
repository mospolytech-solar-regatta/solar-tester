#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta

import serial

from config.models import BoatTestConfig

cfg = BoatTestConfig().from_file()
CONFIG_NAME = 'boat'
INTERVAL = 1
RUN = True


def main():
    port = serial.Serial(cfg.serial_config.name, cfg.serial_config.rate, timeout=0,
                         parity=serial.PARITY_EVEN, rtscts=1)
    data = cfg.get_data()
    last_timestamp = datetime.now()
    while RUN:
        for data_frame in data:
            if datetime.now() - last_timestamp > timedelta(seconds=INTERVAL):
                last_timestamp = datetime.now()
                data_frame['created_at'] = datetime.now()
                payload = json.dumps(data_frame, default=str) + '\n'
                port.write(payload.encode('utf-8'))


if __name__ == '__main__':
    main()
