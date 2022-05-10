#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from config.models import BoatTestConfig
from datetime import datetime, timedelta
import serial

cfg = BoatTestConfig().from_file()
config_name = 'boat'
interval = 1
run = True


def main():
    port = serial.Serial(cfg.serial_config.name, cfg.serial_config.rate, timeout=0,
                         parity=serial.PARITY_EVEN, rtscts=1)
    data = cfg.get_data()
    last_timestamp = datetime.now()
    while run:
        for d in data:
            if datetime.now() - last_timestamp > timedelta(seconds=interval):
                last_timestamp = datetime.now()
                d['created_at'] = datetime.now()
                payload = json.dumps(d, default=str)
                port.write(payload.encode('utf-8'))


if __name__ == '__main__':
    main()
