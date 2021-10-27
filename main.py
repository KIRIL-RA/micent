import datetime
from os import truncate
from requests.models import Response
import log_functions
import adapter
import server
from threading import Timer

# Const parametrs
MAX_TEMPERATURE = 20
MIN_TEMPERATURE = 17
PUMP_START_PERIOD = 0
PUMP_STOP_PERIOD = 2
PUMP_SECONDS = 10
START_LAMP_HOUR = 6
STOP_LAMP_HOUR = 22
VENTILATION_SECONDS = 600
COOLING_SECONDS = 3000
FETCH_SECONDS = 5

Auto = True
cooling_mode = 0 # Mode 0 - cooling, mode 1 - heating
response = 0
Last_ventilation_hour = 0
Last_pump_day = 0

cooling = False
Ventilation = False
Light1 = False
Pump = False

Temperature = 0
Humidity = 0
Water_level = 0

now = datetime.datetime.now()

def fetch():
    global response, Auto, Temperature, cooling, cooling, Ventilation, Light1, Pump, Light1, Water_level, now

    # Send data to server
    if Auto == True:
        response = server.send_all(Light1, cooling, Ventilation, Pump, Temperature, Humidity, Water_level, now)
    else:
        response = server.send_sensors(Temperature, Humidity, Water_level, now)

    # Handing recieved data
    if response != False:
        Auto = bool(int(response['auto']))
    else:
        Auto = True

    Timer(FETCH_SECONDS, fetch).start()

def check_temperature():
    global Temperature, cooling, cooling_mode

    # If cooling mode - cooling
    if cooling_mode == 0:
        if Temperature >= MAX_TEMPERATURE:
            log_functions.file_log(now, "Conditon continued")
            Timer(COOLING_SECONDS, check_temperature).start()
        else:
            cooling = False
            log_functions.file_log(now, "Conditon stoped")
    
    # If cooling mode - heating
    elif cooling_mode == 1:
        if Temperature <= MIN_TEMPERATURE:
            log_functions.file_log(now, "Heating continued")
            Timer(COOLING_SECONDS, check_temperature).start()
        else:
            cooling = False
            log_functions.file_log(now, "Heating stoped")

def ventilation_stop():
    # Stop ventilation
    global Ventilation
    Ventilation = False
    log_functions.file_log(now, "Ventilation stoped")

def pump_stop():
    # Stop pump
    global Pump
    Pump = False
    log_functions.file_log(now, "Pump stoped")

def logic():
    global cooling, Ventilation, Light1, Last_ventilation_hour, Pump, Last_pump_day, now

    # If now is the watering period and there was no watering on that day
    if now.hour <= PUMP_STOP_PERIOD and now.hour >= PUMP_START_PERIOD and Last_pump_day != now.day:
        Last_pump_day = now.day
        Pump = True
        log_functions.file_log(now, "Pump started")
        Timer(PUMP_SECONDS, pump_stop).start()

    # If cooling mode - cooling
    if cooling_mode == 0:

        # If the temperature is higher than normal and cooling not working, turn on the cooling
        if Temperature >= MAX_TEMPERATURE and cooling == False:
            cooling = True
            log_functions.file_log(now, "Conditon started")
            Timer(COOLING_SECONDS, check_temperature).start()

    # If cooling mode - heating
    elif cooling_mode == 1:

        # If the temperature is less than normal and heating not working, turn on the cooling
        if Temperature <= MIN_TEMPERATURE and cooling == False:
            cooling = True
            log_functions.file_log(now, "Heating started")
            Timer(COOLING_SECONDS, check_temperature).start()
    
    # Turn on the ventilation once an hour
    if now.hour != Last_ventilation_hour:
        Last_ventilation_hour = now.hour
        Ventilation = True
        log_functions.file_log(now, "Ventilation started")
        Timer(VENTILATION_SECONDS, ventilation_stop).start()

    # If the period of illumination and the light is not turned on, then turn on
    if now.hour < STOP_LAMP_HOUR and now.hour >= START_LAMP_HOUR and Light1 == False:
        log_functions.file_log(now, "Light on")
        Light1 = True
    
    # Turn off
    elif Light1 == True:
        log_functions.file_log(now, "Light off")
        Light1 = False

def manual_logic():
    global cooling, Ventilation, Light1, Pump

    # Managing devices in manual mode from the site
    cooling = bool(int(response['cooling']))
    Ventilation = bool(int(response['ventilation']))
    Light1 = bool(int(response['light1']))
    Pump = bool(int(response['pump']))

def main():
    global now, Humidity, Temperature, Auto, Water_level

    while True:
        now = datetime.datetime.now()

        Humidity, Temperature, Water_level = adapter.get()

        if(Auto == True): logic()
        else: manual_logic()

        adapter.control(cooling, Ventilation, Light1, Pump)
        log_functions.console_log(cooling, Ventilation, Light1, Temperature, Humidity, Pump, now)

if __name__ == "__main__":
    adapter.initialize()
    fetch()
    main()