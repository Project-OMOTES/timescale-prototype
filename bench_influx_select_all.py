import time

from influxdb import InfluxDBClient


"""
Takes about ~20 seconds of processing at InfluxDB-side (and uses A LOT of memory).
Data is received & parsed by this script after 66 seconds.
After the query, influxdb stays at ~6GB of memory in use.
"""

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'energy_profiles')
before = time.time()
result = client.query("select HeatIn_Q1 from \"febb2e58-2757-4849-bd35-3a1a31636a56\";")
after = time.time()
print(f'It took {after - before} seconds.')
print("Result: ", len(list((result.get_points()))))
