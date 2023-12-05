#################################
# CSC 102 Defuse the Bomb Project
# Main program
# Team: Gourd
#################################

# import the configs
from bomb_configs import *
# import the phases

import bomb_phases 
from tkinter import *
import tkinter
from threading import Thread
import pygame
from time import sleep
import os
import sys

###########
# functions
###########
# generates the bootup sequence on the LCD

# sets up the phase threads
def setup_phases():
    global timer, keypad, wires, button, toggles
    
    # setup the timer thread
    timer = Timer(component_7seg, COUNTDOWN)
    # bind the 7-segment display to the LCD GUI so that it can be paused/unpaused from the GUI
    gui.setTimer(timer)
    # setup the keypad thread
    keypad = Keypad(component_keypad, keypad_target)
    # setup the jumper wires thread
    wires = Wires(component_wires, wires_target, display_length=5)
    # setup the pushbutton thread
    button = Button(component_button_state, component_button_RGB, button_target, button_color, timer)
    # bind the pushbutton to the LCD GUI so that its LED can be turned off when we quit
    gui.setButton(button)
    # setup the toggle switches thread
    toggles = Toggles(component_toggles, toggles_target, display_length=4)

    # start the phase threads
    timer.start()
    keypad.start()
    wires.start()
    button.start()
    toggles.start()
    
    # play the tick audio
    pygame.mixer.music.load(TICK)
    pygame.mixer.music.play(-1)

    # check the phases
    gui.after(100, check_phases)

# checks the phase threads
def check_phases():
    global active_phases, exploding

    # restart the tick audio if needed
    if (not exploding and not pygame.mixer.music.get_busy()):
        pygame.mixer.music.load(TICK)
        pygame.mixer.music.play(-1)
        
    # check the timer
    if (timer._running):
        # update the GUI
        gui._ltimer["text"] = f"Time left: {timer}"
        # play the exploding audio at t-10s
        if (not exploding and timer._interval * timer._value <= 11.25):
            exploding = True
            component_7seg.blink_rate = 1
            pygame.mixer.music.load(EXPLODING)
            pygame.mixer.music.play(1)
        if (timer._value == 60):
            gui._ltimer["fg"] = "#ff0000"
    else:
        # the countdown has expired -> explode!
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(100, gui.conclusion, exploding, False)
        # don't check any more phases
        return
    # check the keypad
    if (keypad._running):
        # update the GUI
        gui._lkeypad["text"] = f"Combination: {keypad}"
        # the phase is defused -> stop the thread
        if (keypad._defused):
            keypad._running = False
            gui._lkeypad["fg"] = "#00ff00"
            defused()
        # the phase has failed -> strike
        elif (keypad._failed):
            strike()
            # reset the keypad
            keypad._failed = False
            keypad._value = ""
    # check the wires
    if (wires._running):
        # update the GUI
        gui._lwires["text"] = f"Wires: {wires}"
        # the phase is defused -> stop the thread
        if (wires._defused):
            wires._running = False
            gui._lwires["fg"] = "#00ff00"
            defused()
        # the phase has failed -> strike
        elif (wires._failed):
            strike()
            # reset the wires
            wires._failed = False
    # check the button
    if (button._running):
        # update the GUI
        gui._lbutton["text"] = f"Button: {button}"
        # the phase is defused -> stop the thread
        if (button._defused):
            button._running = False
            gui._lbutton["fg"] = "#00ff00"
            defused()
        # the phase has failed -> strike
        elif (button._failed):
            strike()
            # reset the button
            button._failed = False
    # check the toggles
    if (toggles._running):
        # update the GUI
        gui._ltoggles["text"] = f"Toggles: {toggles}"
        # the phase is defused -> stop the thread
        if (toggles._defused):
            toggles._running = False
            gui._ltoggles["fg"] = "#00ff00"
            defused()
        # the phase has failed -> strike
        elif (toggles._failed):
            strike()
            # reset the toggles
            toggles._failed = False

    # note the strikes on the GUI
    gui._lstrikes["text"] = f"Strikes left: {strikes_left}"
    # too many strikes -> explode!
    if (strikes_left == 0):
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(1000, gui.conclusion, exploding, False)
        # stop checking phases
        return
    # a few strikes left -> timer goes twice as fast!
    elif (strikes_left == 2 and not exploding):
        timer._interval = 0.5
        gui._lstrikes["fg"] = "#ff0000"
    # one strike left -> timer goes even faster!
    elif (strikes_left == 1 and not exploding):
        timer._interval = 0.25

    # the bomb has been successfully defused!
    if (active_phases == 0):
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(100, gui.conclusion, exploding, True)
        # stop checking phases
        return

    # check the phases again after a slight delay
    gui.after(100, check_phases)

# handles a strike
def strike():
    global strikes_left
    
    # note the strike
    strikes_left -= 1
    # play the strike audio
    if (not exploding):
        pygame.mixer.music.load(STRIKE)
        pygame.mixer.music.play(1)

# handles when a phase is defused
def defused():
    global active_phases

    # note that the phase is defused
    active_phases -= 1
    # play the defused audio
    if (not exploding):
        pygame.mixer.music.load(DEFUSED)
        pygame.mixer.music.play(1)

# turns off the bomb
def turn_off():
    # stop all threads
    timer._running = False
    keypad._running = False
    wires._running = False
    button._running = False
    toggles._running = False

    # turn off the 7-segment display
    component_7seg.blink_rate = 0
    component_7seg.fill(0)
    # turn off the pushbutton's LED
    for pin in button._rgb:
        pin.value = True

######
# MAIN
######

# initialize pygame
pygame.init()

# initialize the LCD GUI
window = Tk()

gui = bomb_phases.Lcd(window)




# initialize the bomb strikes, active phases (i.e., not yet defused), and if the bomb is exploding
strikes_left = NUM_STRIKES
active_phases = NUM_PHASES
exploding = False

# "boot" the bomb
#gui.after(1000, bootup)

# display the LCD GUI
window.mainloop()
