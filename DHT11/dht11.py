class DHT11:
    'DHT11 class using Inductrial I/O driver'

    def __init__(self):
        return


    def readTemp(self):
        while True:
            try:
                with open('/sys/bus/iio/devices/iio:device0/in_temp_input') as f:           
                    str = f.read()
                return int(str) // 1000
            except IOError:
                continue

    def readHumidity(self):
        while True:
            try:
                with open('/sys/bus/iio/devices/iio:device0/in_humidityrelative_input') as f:           
                    str = f.read()
                return int(str) // 1000
            except IOError:
                continue

        
