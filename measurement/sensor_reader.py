from pyA20.gpio import gpio

import dht
import riprova
import sqlite3
import time
import multiprocessing


from collections import namedtuple
import random
import math

# initialize GPIO
# DHT22_PIN = port.PA13


class Measurer:
    def __init__(self, pin):
        self.sensor = self._init_sensor(pin)
        self.db_conn = sqlite3.connect('measurement_db.db', isolation_level=None)

    @riprova.retry(backoff=riprova.ConstantBackoff(interval=2, retries=5))
    def _read(self):
        result = self.sensor.read()
        if not result.is_valid():
            raise ValueError('Reading not valid !')
        return result

    def _save_to_db(self, temperature, humidity):
        cur = self.db_conn.cursor()
        cur.execute('INSERT INTO measurements(temperature, humidity) VALUES (?, ?);', (temperature, humidity))
        cur.close()

    def _init_sensor(self, pin):
        gpio.init()
        return dht.DHT22(pin=pin)

    def do(self):
        while True:
            try:
                result = self._read()
                self._save_to_db(result.temperature, result.humidity)
            except Exception as e:
                print(e)
            finally:
                time.sleep(60)

    def spawn_process(self):
        process = multiprocessing.Process(target=self.do)
        process.start()


class Mocker(Measurer):
    result = namedtuple('result', ['temperature', 'humidity'])

    def _init_sensor(self, pin):
        return None

    def _read(self):
        return self.result(temperature=math.fabs(random.random()*40), humidity=random.randint(10, 100))




