import MessageManager
# import can
# import os
# import time

start=time.time()
runtime=10 #How long?
end=start+runtime
now=time.time()

os.system('sudo ip link set can0 up type can bitrate 250000')
time.sleep(0.1)

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

except OSError:
    print('Cannot find PiCAN board.')
    exit()


while now < end:

    now = time.time()

    message = bus.recv()

#   message_send = bus.send()

    my_message = MessageManager.MessageTransceiver(message)

    my_message.listen_data()

    my_message.check_message_type()

    print(my_message.pgn_number)

    if my_message.pgn_number == 0:
        print('Vehicle Odometer Data Found')
        module = MessageManager.OdometerData(my_message)

    if my_message.pgn_number == 3:
        print('Fuel Economy Data Found')
        module = MessageManager.FuelEconomyData(my_message)

    if my_message.pgn_number == 4:
        print('Fuel Level Data Found')
        module = MessageManager.FuelLevelData(my_message)

    # print(module.dataField)
    print(module.calculate_element())





