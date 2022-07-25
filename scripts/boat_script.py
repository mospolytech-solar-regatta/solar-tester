#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta

import serial

CONFIG_NAME = 'boat'
INTERVAL = 1
RUN = True


def boat_script(config, controller):
    port = serial.Serial(config.serial_config.name, config.serial_config.rate, timeout=0,
                         parity=serial.PARITY_EVEN, rtscts=1)
    data = config.get_data()
    last_timestamp = datetime.now()
    while controller.State == controller.STATES.RUN:
        for data_frame in data:
            if datetime.now() - last_timestamp > timedelta(seconds=INTERVAL):
                last_timestamp = datetime.now()
                data_frame['created_at'] = datetime.now()
                payload = json.dumps(data_frame, default=str) + '\n'
                port.write(payload.encode('utf-8'))
