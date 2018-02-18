import can
import time
import os


class MessageTransceiver:

    pgns = ['fee0', 'fee5', 'fee9', 'fef2', 'fefc']
    unprocessedMessage = 'null'
    # flag to  check if it is a required message
    messageFlag = 0
    pgn_number = 0

    def __init__(self):
        print('Message object created.')
        # message = bus.recv()


    def listen_data(self, message):
        self.unprocessedMessage = str(message)

    def check_message_type(self):
        # Loop through and check if pgn is required pgn
        for x in range(0, 5):
            substring = self.pgns[x]

            check = self.unprocessedMessage.find(substring)
            # if message contains a required parameter, set a flag and save the pgn number
            if check > -1:
                self.messageFlag = 1
                self.pgn_number = x


class ModuleData:

    parameterGroupNumber = -1
    dataField = 'null'
    message = 'null'
    pgnNames = ['Vehicle Odometer', 'Total Engine Hours', 'Total Fuel Used', 'Average Fuel Economy', 'Fuel Level 1']

    # Constructor
    def __init__(self, message_received):
        self.message = message_received.unprocessedMessage
        self.dataField = self.message[51:]
        self.parameterGroupNumber = message_received.pgn_number


# Odometer data inherits from module data
class OdometerData(ModuleData):

    # Constants for data processing
    resolution = 0.125
    conversion_constant = 0.621371
    total_miles = -1

    def __init__(self, message_received):
        ModuleData.__init__(self,  message_received)

    # method to calculate the required data element from the message
    def calculate_element(self):

        # find the last index
        indexLast = len(self.dataField) - 1

        # Grab each data byte and reverse the order
        set1 = self.dataField[indexLast - 1] + self.dataField[indexLast]

        set2 = self.dataField[indexLast - 4] + self.dataField[indexLast - 3]

        set3 = self.dataField[indexLast - 7] + self.dataField[indexLast - 6]

        set4 = self.dataField[indexLast - 10] + self.dataField[indexLast - 9]

        reverse = set1 + set2 + set3 + set4

        hex_converted = int(reverse, 16)

        kilometers = 0.125 * hex_converted

        miles = kilometers * self.conversion_constant

        print('Odometer in Miles: ')
        print(miles)
        return miles


# FuelEconomyData inherits from ModuleData
class FuelEconomyData(ModuleData):

        # Constants for data conversion and processing
        resolution = (1/512)
        conversion_constant = 0.62131192 * (1/0.2641762)
        miles_per_gallon = -1

        def __init__(self, message_received):
            ModuleData.__init__(self, message_received)

        def calculate_element(self):

            # Get the last index
            indexLast = len(self.dataField) - 1

            # Grab each data byte and reverse the order
            set1 = self.dataField[indexLast - 7] + self.dataField[indexLast-6]

            set2 = self.dataField[indexLast - 10] + self.dataField[indexLast - 9]

            reverse = set1 + set2

            decimal = int(reverse, 16)

            self.miles_per_gallon = decimal * self.conversion_constant * self.resolution

            print('Fuel Economy in mpg: ')
            print(self.miles_per_gallon)

            return self.miles_per_gallon
