#!/usr/bin/python

import RPi.GPIO as GPIO
import sys, getopt 
from time import sleep

def setRelay(relay_pin, gpio_mode=GPIO.BOARD, power_on = GPIO.HIGH, switch = False, delay = 0, debug = False):

    if gpio_mode == GPIO.BOARD:
        ports = [3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26,29,31,32,33,35,36,37,38,40]
    else:
        ports = [2,3,4,17,27,22,10,9,11,5,6,13,19,26,14,15,18,23,24,25,8,7,12,16,20,21]

    if debug:
        print "Board mode: " + str(gpio_mode)
        print "PIR pin:    " + str(relay_pin)

    try:
        GPIO.setwarnings(False)
        GPIO.setmode(gpio_mode) 
        
        if relay_pin in ports:
            GPIO.setup(relay_pin, GPIO.OUT)    # set output

        else:
            print "\nERROR: pin is not an valid input."
            helper()

        if switch:
            power_on = not GPIO.input(relay_pin)

        sleep(delay)

        GPIO.output(relay_pin, power_on)

    except:
        print "Something wrong"
        GPIO.cleanup()

    finally:
        if debug:
            print "\nEnd of program.\n"


def helper():
    sys.exit('''\

Usage: %s --relay-pin n [--power-off | --power-off] [--switch] [--gpio-mode BCM] [--delay s] [--debug]

Options:

-p --relay-pin n   parameter "n" is pin number, where relay is connected

-1 --power-on      (default) power on relay

-0 --power-off     power off relay

-s --switch        switch relay to opposite state

-d --delay s       where "s" is delay in seconds; default = 0

-m --gpio-mode     GPIO pin numbering mode. Valid options:
                     BOARD - (default) pin number referring to number on board 
                     BCM   - pin number corresponds to Broadcom SOC channel
                    
-v --debug         display debug information

    ''' % sys.argv[0])


if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:],"v01sd:p:m:",["verbose","debug","relay-pin=","gpio-mode=","power-on","power-off","switch","delay"])

    except getopt.GetoptError:
        helper()

    debug = False
    gpio_mode = GPIO.BOARD
    relay_pin = ""
    power_on = GPIO.HIGH
    switch = False
    delay = 0

    for opt, arg in opts:

        if opt in ["--debug","-v","--verbose"]:
            print "Running in debug mode."
            debug = True

        elif opt in ["-p","--relay-pin"]:
            if arg.isdigit():
                relay_pin = int(arg)
            else:
                print "\nERROR: Invalid pin number."
                helper()
        elif opt in ["-m","--gpio-mode"]:
            if arg == "BCM":
                gpio_mode = GPIO.BCM
            elif arg not in ["BCM","BOARD"]:
                print "\nERROR: Unknown GPIO board mode."
                helper()
        elif opt in ["-0", "--power-off"]:
            power_on = GPIO.LOW
        elif opt in ["-s", "--switch"]:
            switch = True
        elif opt in ["-d", "--delay"]:
            if arg.isdigit():
                delay = int(arg)
            else:
                print "\nERROR: Invalid delay"
                helper()

        elif opt not in ["-1", "--power-on"]:   # default values
            helper()

    if relay_pin == "":
        print "\nERROR: undefined pin."
        helper()

    setRelay(relay_pin, gpio_mode, power_on, switch, delay, debug)
