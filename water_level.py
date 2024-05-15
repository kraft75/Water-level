"""
Entwickle anhand des vorgegebenen Codes eines Wasserstandsensors,
die Funktion, dass ein Füllstand zu erkennen ist.

Als zusätzliche Extra Herausforderung entwerfe den Sensor anlernbar. Dies bedeutet,
dass per Tastendruck ein minimaler und ein maximaler Füllstand angelernt werden.

Aus den Werten soll der prozentuale Füllstand berechnet und auf einer LED-Lichtorgel
angezeigt werden.
Nutze hierfür beispielsweise ein Wasserglas.
"""

from machine import Pin, PWM, ADC, SoftI2C
from time import sleep
from lcd_api import LcdApi
from i2c_lcd import I2cLcd



# Pin (Wassersensor) mit ADC verbinden
adc = ADC(Pin(35, Pin.IN))
# Button definieren
buttonSet = Pin(12,Pin.IN, Pin.PULL_UP)

""" LEDs mit PWM-Objekten verknüpfen. Justierung der Helligkeit """
red1 = Pin(14,Pin.OUT)
pwm_redR = PWM(red1)

blue1 = Pin(27,Pin.OUT)
pwm_blueR = PWM(blue1)

white1  = Pin(26,Pin.OUT)
pwm_whiteR = PWM(white1)

white2  = Pin(25,Pin.OUT)
pwm_whiteL = PWM(white2)

blue2 = Pin(33,Pin.OUT)
pwm_blueL = PWM(blue2)

red2 = Pin(32,Pin.OUT)
pwm_redL = PWM(red2)


# Pulsweite 
duty_cycle = 0
# Bei Programmstart sind die LEDs aus
pwm_redR.duty(duty_cycle)
pwm_redL.duty(duty_cycle)
pwm_whiteL.duty(duty_cycle)
pwm_whiteR.duty(duty_cycle)
pwm_blueR.duty(duty_cycle)
pwm_blueL.duty(duty_cycle)
# Maximal Wert für den Füllstand
maxi = 0
# Variablen für die Schwellwerte
zk1 = 0
zk2 = 0


""" LCD einrichten zur Ausgabe der Sensorwerte """
# LCD Speicheradresse und Größenangabe des Bildschirms
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16
# I2C mit Pins und gegebener Taktung
i2c = SoftI2C(scl = Pin(22), sda = Pin(21), freq = 10000)
# LCD-Monitor
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

""" Schleife zur Berechnung der Sensorwerte, die den
    Füllstand anhand der LEDs anzeigen
"""
PAUSE = 0.5
counter = 0
liste = []
while True:
    lcd.clear()
    # Sensorwerte auslesen
    wert = adc.read() 
    lcd.putstr("Value: " + str(wert))
    print("Value: " + str(wert))
    start = buttonSet.value()
    
    #Bei Knopfsruck...
    if start:
        # ... wird der Maximalwert aus der Liste bestimmt
        maxi = max(liste)
        print("Max ", maxi)
        # ... und davon die obere Schranke zk2 errechnet
        zk2 = maxi * 0.8
        print("z2 ", zk2)
        # ... als auch die untere Schranke
        zk1 = maxi * 0.2
        print("z1 ", zk1)
        #Liste wird anschließend gelöscht
        liste.clear()
        
        sleep(0.3)
        
    else:
        
        #print("Liste. " + str(liste))
        pass
        sleep(PAUSE)
        
    # Bei Messwert null bleiben die LEDs inaktiv   
    if wert == 0:
        print("LED aus")
        pwm_redR.duty(0)
        pwm_redL.duty(0)
        pwm_whiteL.duty(0)
        pwm_whiteR.duty(0)
        pwm_blueR.duty(0)
        pwm_blueL.duty(0)
        
    # Messwert zw. null und erstem Schwellwert:
    # Leuchten der ersten beiden LEDs     
    elif wert > 0 and wert <= zk1:
        print("LED 1+2")
        pwm_redL.duty(512)
        pwm_blueL.duty(512)
        pwm_redR.duty(0)
        pwm_whiteL.duty(0)
        pwm_whiteR.duty(0)
        pwm_blueR.duty(0)
        
    # Messwert zwischen zw. erstem und zweitem Schwellwert:
    # Leuchten der mittleren zwei LEDs
    elif wert > zk1 and wert <= zk2:
        print("LED 3+4")
        pwm_redR.duty(0)
        pwm_redL.duty(0)
        pwm_whiteL.duty(512)
        pwm_whiteR.duty(512)
        pwm_blueR.duty(0)
        pwm_blueL.duty(0)
        
    # Messwert oberhalb des zweiten Schwellwerts:
    # Leuchten der letzten beiden LEDs
    elif wert > zk2:
        print("LED 5+6")
        pwm_blueR.duty(512)
        pwm_redR.duty(512)
        pwm_redL.duty(0)
        pwm_blueL.duty(0)
        pwm_whiteL.duty(0)
        pwm_whiteR.duty(0)
        
    # Speichert Sensorwerte in die Liste
    liste.append(wert)
    print("Liste: ", liste)

    
    # Nach 100 Iterationen Liste automatisch löschen
    # counter auf null zurücksetzen
    if counter > 100:
        liste.clear()
        counter = 0
        
    counter += 1
    sleep(PAUSE)
     

    
    
   