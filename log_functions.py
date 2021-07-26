def console_log(Condition, Ventilation, Light1, Temperature, Humidity, now):
    print("--Condition: " + str(Condition) + " --Ventilation: " + str(Ventilation) + " --Light1: " + str(Light1) + " --Humidity: " + str(Humidity) + " --Temperature: " + str(Temperature) + " --Time: " + str(now), end="\r")

def file_log(Time, Event):
    f = open("log.csv", "a")
    print(str(Time) + " : " + Event)
    f.write(str(Time) + ", " + Event + "\n")
    f.close()
    
