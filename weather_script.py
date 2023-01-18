#!/usr/bin/python
from sense_hat import SenseHat
import time
import sys
import math
from ISStreamer.Streamer import Streamer  

sense = SenseHat()
logger = Streamer(bucket_name="Sense Hat Sensor Data", access_key="YOUR_KEY_HERE")  
sense.clear()

try:
      while True:
          temp = sense.get_temperature()
          temp = round(temp, 1)            # Temperatur in °C
          TK = temp + 273.15               # Temperatur in Kelvin
          logger.log("Temperatur in °C",temp)

          humidity = sense.get_humidity() 
          humidity = round(humidity, 1)   # Relative Luftfeuchte 
          logger.log("Relative Luftfeuchtigkeit:",humidity)  

          pressure = sense.get_pressure() 
          pressure = round(pressure, 1)    # Luftdruck
          logger.log("Luftdruck:",pressure)
            
          if temp >= 0:
               a = 7.5
               b = 237.3
          elif temp < 0: # T < 0 über Wasser (Taupunkt)
               a = 7.6
               b = 240.7            
          #else temp < 0 über Eis (Frostpunkt)
          #    a = 9.5
          #    b = 265.5

          R = 8314.3 # J/(kmol*K) (universelle Gaskonstante)
          m = 18.016 # kg/kmol (Molekulargewicht des Wasserdampfes)

          SDD1 = 6.1078 * 10**((a*temp)/(b+temp)) # SDD(T): Sättigungsdampfdruck in hPa
          DD = humidity/100 * SDD1 # Dampfdruck in hPa
          v = math.log(DD/6.1078, 10) # Logarithmus zur Basis 10
          TD = b*v/(a-v) # Taupunkttemperatur in °C
          SDD2 = 6.1078 * 10**((a*TD)/(b+TD)) # SDD(TD): Sättigungsdampfdruck in hPa
          r = 100 * SDD2 / SDD1 # relative Luftfeuchte
          AF1= 10**5 * m/R * DD/TK # AF(r,TK) - Absolute Feuchte in g Wasserdampf pro m^3 Luft (in Abhängigkeit von der relativen Luftfeuchte und Temperatur in Kelvin)
          AF2 = 10**5 * m/R * SDD2/TK # AF(TD,TK) - Absolute Feuchte in g Wasserdampf pro m^3 Luft (in Abhängigkeit von der Taupunkttemperatur in °C und Temperatur in Kelvin)

          TDr = round(TD,1) # Taupunkttemperatur in °C, gerundet auf zwei Nachkommastellen
          logger.log("Taupunkt in Grad Celsius:",TDr)

          WUG = (temp - TD) * 125 # Wolkenuntergrenze  in Meter (Faustregel)
          logger.log("Wolkenuntergrenze  in Meter:",round(WUG,1))

          time.sleep(1)
except KeyboardInterrupt:
     pass
