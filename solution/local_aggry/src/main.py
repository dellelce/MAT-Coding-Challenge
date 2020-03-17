"""
MAT Test Aggregrator

formatting using default yapf configuration
"""

import json
import random
import os
from math import sqrt, pow
from math import radians, sin, cos, asin
from time import sleep

from paho.mqtt.client import Client

car_count = int(os.environ.get('CAR_COUNT') or 6)
debug = os.environ.get('DEBUG').lower() == 'true' or False
subs = 'carCoordinates'

# create an array to keep state of cars
cars = [None for car in range(car_count)]

# track who is on top
car_total = [0 for car in range(car_count)]
car_top = 0


def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two coords"""
    R = 6372.8  # Earth radius in kilometers

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2)**2 + cos(lat1) * cos(lat2) * sin(dLon / 2)**2
    c = 2 * asin(sqrt(a))

    return R * c


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(subs)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    # shared data
    global cars, car_total, car_top

    carEvent = None
    carCoordinates = json.loads(msg.payload)

    carIndex = carCoordinates["carIndex"]
    timestamp = carCoordinates["timestamp"]

    curPosition = {
        "timestamp":
        timestamp,
        "location":
        (carCoordinates["location"]["lat"], carCoordinates["location"]["long"])
    }

    if cars[carIndex] is None:
        cars[carIndex] = curPosition
        print("initial position: car {} at {}".format(carIndex,
                                                      str(curPosition)))
    else:
        oldPosition = cars[carIndex]

        # travelled in last "step"
        pos_diff = haversine(curPosition["location"][0],
                             curPosition["location"][1],
                             oldPosition["location"][0],
                             oldPosition["location"][1])

        car_total[carIndex] += pos_diff

        new_leader = car_total.index(max(car_total)) + 1

        if new_leader != car_top:
            if car_top != 0:
                carEvent = {
                    "timestamp":
                    timestamp,
                    "text":
                    "Car {} races ahead of Car {} in a dramatic overtake.".
                    format(new_leader, car_top)
                }
            car_top = new_leader

        # km to m factor: 0.621371
        # I am missing something here
        speed_mph = pos_diff * 3600 * 0.621371

        # find this car position
        my_total = car_total[carIndex]
        my_position = sorted(car_total).index(my_total) + 1

        carPosition = {
            "timestamp": timestamp,
            "carIndex": carIndex + 1,
            "type": "POSITION",
            "value": my_position
        }

        carSpeed = {
            "timestamp": timestamp,
            "carIndex": carIndex + 1,
            "type": "SPEED",
            "value": speed_mph
        }

        # save received position
        cars[carIndex] = curPosition

        # publish messages
        client.publish('carStatus', payload=json.dumps(carSpeed))
        client.publish('carStatus', payload=json.dumps(carPosition))

        # this is only sent when there is a new leader
        if carEvent is not None:
            client.publish('events', payload=json.dumps(carEvent))


if debug:

    def on_log(client, userdata, level, string):
        print("on_log: {} {}".format(str(level), string))


def main():
    print("Hello! this is aggry! I send wonderful data :)")

    client = Client(client_id="aggry")
    client.on_connect = on_connect
    client.on_message = on_message

    if debug:
        client.on_log = on_log
    else:
        print("Debug mode disabled by configuration.")

    # Swarm does not handle dependencies
    sleep(2)

    try:
        rc = client.connect("broker", 1883, 60)
    except:
        # just try again
        print("connect: trying again...")
        sleep(4)
        client.connect("broker", 1883, 60)

    # main loop
    client.loop_forever()


if __name__ == '__main__':
    main()
