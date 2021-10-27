import requests

def send_all(Light1, cooling, Ventilation, Pump, Temperature, Humidity, Water_level, Now):
    # Send all states
    try:
        request = requests.get("http://a0585513.xsph.ru/get?update=all&light1=" + str(int(Light1)) + "&cooling=" + str(int(cooling)) + "&ventilation=" + str(int(Ventilation)) + "&pump=" + str(int(Pump)) + "&temperature=" + str(Temperature) + "&humidity=" + str(Humidity) +  "&water_level=" + str(Water_level) + "&time=" + str(Now))
        response = request.json()
        return response
    except Exception as e:
        print(e)
        return False

def send_sensors(Temperature, Humidity, Water_level, Now):
    # Send only sensor states
    try:
        request = requests.get("http://a0585513.xsph.ru/get?update=sensors&temperature=" + str(Temperature) +  "&humidity=" + str(Humidity) + "&water_level=" + str(Water_level) + "&time=" + str(Now))
        response = request.json()
        return response
    except Exception as e:
        print(e)
        return False