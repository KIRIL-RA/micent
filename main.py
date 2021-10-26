import datetime

from requests.models import Response
import log_functions
import adapter
import server
from threading import Timer

MAX_TEMPERATURE = 22
START_LAMP_HOUR = 6
STOP_LAMP_HOUR = 22
VENTILATION_SECONDS = 10
CONDITION_SECONDS = 10 #1800
UPDATE_SECONDS = 30

auto = False
response = 0

Condition = False
Ventilation = False
Light1 = False

Temperature = 0
Humidity = 0
Last_ventilation_hour = 0

now = datetime.datetime.now()

def update():
    global response, auto
    response = server.make_request()
    auto = bool(int(response['auto']))
    Timer(UPDATE_SECONDS, update).start()

def check_temperature():
    global Temperature, Condition

    if Temperature >= MAX_TEMPERATURE:
        log_functions.file_log(now, "Conditon continued")
        Timer(CONDITION_SECONDS, check_temperature).start()
    else:
        Condition = False
        log_functions.file_log(now, "Conditon stoped")

def ventilation_stop():
    global Ventilation
    Ventilation = False
    log_functions.file_log(now, "Ventilation stoped")

def logic():
    global Condition, Ventilation, Light1, Last_ventilation_hour, now

    if Temperature >= MAX_TEMPERATURE and Condition == False:
        Condition = True
        log_functions.file_log(now, "Conditon started")
        Timer(CONDITION_SECONDS, check_temperature).start()
    
    if now.hour != Last_ventilation_hour:
        Last_ventilation_hour = now.hour
        Ventilation = True
        log_functions.file_log(now, "Ventilation started")
        Timer(VENTILATION_SECONDS, ventilation_stop).start()

    if STOP_LAMP_HOUR  < now.hour >= START_LAMP_HOUR :
        if(Light1 == False):
            log_functions.file_log(now, "Light on")
            Light1 = True
    
    elif Light1 == True:
        log_functions.file_log(now, "Light off")
        Light1 = False

def manual_logic():
    pass#print("manual mode")

def main():
    global now, Humidity, Temperature
    update()
    Timer(UPDATE_SECONDS, update).start()

    while True:
        now = datetime.datetime.now()

        Humidity, Temperature = adapter.get()

        if(auto == False): logic()
        else: manual_logic()
        adapter.control(Condition, Ventilation, Light1)
        #log_functions.console_log(Condition, Ventilation, Light1, Temperature, Humidity, now)

if __name__ == "__main__":
    main()