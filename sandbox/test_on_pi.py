import sys
import time
import numpy as np
import pylab as pl
import tables as pytb
import os
sys.path.append('../')

from vent.controller.control_module import get_control_module, Balloon_Simulator
from vent.common.message import SensorValues, ControlSetting
from vent.common.values import ValueName, CONTROL

Controller = get_control_module(sim_mode=False)

def do_stuff():
    
    Controller.start()
    p_store = np.zeros((1000,2))
    idx = 0

    for t in np.arange(0, 30, 0.05):
        if t%5==0:  # ask for a heartbeat from thread every 5 seconds
            print(t)

        ## Do things
        command = ControlSetting(name=ValueName.PEEP, value=5)
        Controller.set_control(command)
        command = ControlSetting(name=ValueName.PIP, value=25)
        Controller.set_control(command)
        command = ControlSetting(name=ValueName.PIP_TIME, value=0.5)
        Controller.set_control(command)
        command = ControlSetting(name=ValueName.BREATHS_PER_MINUTE, value=15)
        Controller.set_control(command)
        command = ControlSetting(name=ValueName.INSPIRATION_TIME_SEC, value = 1.3)
        Controller.set_control(command)
        ##

        setin = Controller.HAL.setpoint_in
        setex = Controller.HAL.setpoint_ex
        pp    = Controller.HAL.pressure
        print([pp, setin, setex])

        p_store[idx,:] = np.array([time.time(), pp])
        idx += 1

        time.sleep(0.05)

    Controller.HAL.setpoint_in = 0
    Controller.HAL.setpoint_in = 0
    Controller.stop()

    np.save("data_openloop", p_store)

try:
    do_stuff()

except KeyboardInterrupt:
    print("Ctl C pressed - ending program")

    #make sure valves are closed - a few safety extra commands
    Controller.HAL.setpoint_in = 0
    time.sleep(0.05)
    Controller.HAL.setpoint_in = 0
    time.sleep(0.05)
    Controller.HAL.setpoint_in = 0
    Controller.stop()

    Controller.HAL._inlet_valve.close()
    Controller.HAL._control_valve.close()
    if (Controller.HAL.setpoint_in is not 0) or (Controller.HAL.setpoint_ex is not 0):
        print("Cannot close vents:")
        print("Ex: " + str(Controller.HAL.setpoint_ex ))
        print("In: " + str(Controller.HAL.setpoint_in ))