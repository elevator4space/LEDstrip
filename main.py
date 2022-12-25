######################################################################################################################################################

# @project        Space Elevator ▸ LEDs Strip
# @file           main.py
# @author         <info@spacelevator.org>
# @license        Space Elevator 2022

######################################################################################################################################################

from time import sleep
from datetime import datetime
import json
import logging
import sys

import requests
import serial

def parse_config (config_path) -> dict:

    with open(config_path, 'r') as config_file:
        config_data = json.load(config_file)
        return config_data

def get_next_pass (orbital_object,
                   location,
                   API_KEY) -> dict:
    response = requests.get(f'http://satellites.fly.dev/passes/{orbital_object["NORAD_ID"]}', params = {
        'lat': location['latitude'], 'lon': location['longitude'], 'limit': 1
    })
    return response.json()[0]

def main ():
    logging.basicConfig(stream = sys.stdout, format = '%(asctime)s [%(levelname)s] %(message)s', level = logging.INFO)

    # Read configuration
    try:
        config: dict = parse_config('config.json')
    except:
        logging.exception('Could not parse configuration')
        sys.exit(1)

    with serial.Serial(config['serial']['port'], config['serial']['baudrate']) as ser:
        logging.info('Starting')
        while True:
            now = datetime.now()
            satellite_above = False
            try:
                for satellite in config['satellites']:
                    logging.info('Fetching next pass for %s', satellite['name'])
                    next_pass: dict = get_next_pass(satellite, config['location'], config['API_KEY'])
                    rise_time: datetime = datetime.fromtimestamp(next_pass['rise']['utc_timestamp'])
                    set_time: datetime = datetime.fromtimestamp(next_pass['set']['utc_timestamp'])
                    logging.info('elevation=%s rise_time=%s set_time=%s', next_pass['culmination']['alt'], rise_time, set_time)

                    if float(next_pass['culmination']['alt']) > config['criteria']['culmination']:
                        if now >= rise_time and now <= set_time:
                            satellite_above = True
                            logging.info('%s is above our head!', satellite['name'])
                            ser.write(f"{satellite['color'][0]},{satellite['color'][1]},{satellite['color'][2]};".encode())
                        else:
                            logging.info('%s is not yet above our head.', satellite['name'])
                    else:
                        logging.info('%s\'s next pass elevation is too low (%s < %s).', satellite['name'], next_pass['culmination']['alt'], config['criteria']['culmination'])

                if not satellite_above:
                    ser.write(b'0,0,0;')

            except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
                logging.warning('Could not connect to the API')
                continue

            sleep(10)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info('Bye')

######################################################################################################################################################

