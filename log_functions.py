def console_log(Condition, Ventilation, Light1, Temperature, Humidity, Pump, now):
    print("--Condition: " + str(Condition) + " --Ventilation: " + str(Ventilation) + " --Light1: " + str(Light1) + " --Pump: " + str(Pump) + " --Humidity: " + str(Humidity) + " --Temperature: " + str(Temperature) + " --Time: " + str(now), end="\r")

def file_log(Time, Event):
    f = open("log.csv", "a")
    print(str(Time) + " : " + Event, end="\n\r")
    f.write(str(Time) + ", " + Event)
    f.close()
    
