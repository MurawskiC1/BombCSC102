#################################
# CSC 102 Defuse the Bomb Project
# Main program
# Team: Gourd
#################################

# import the configs
from bomb_configs import *
# import the phases
# import the configs
from bomb_configs import *
# other imports
from tkinter import *
import tkinter
from threading import Thread
import pygame
from time import sleep
import time
import random as rng
import os
import sys
#this should save the changes

#########
# classes
class Queue:
    def __init__(self):
        self._data = []
    
    def enqueue(self, d):
        self._data.append(d)
        
    def dequeue(self):
        if len(self._data) > 0:
            temp = self._data[0]
            del self._data[0]
            return temp
        else:
            print('error')
#########
# the LCD display GUI
class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window, bg="black")
        # make the GUI fullscreen
        window.attributes("-fullscreen", True)
        # we need to know about the timer (7-segment display) to be able to pause/unpause it
        self._timer = None
        # we need to know about the pushbutton to turn off its LED when the program exits
        self._button = None
        # setup the initial "boot" GUI
        self.welcome()
        self.phase = 0
        
    
    def erase(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    def welcome(self):
        self.erase()
        welcome = Label(self,bg = "black", fg = "red" ,font=("Courier New", 30),text="Welcome to")
        welcome.grid(row = 0,column = 1)
        title = Label(self,bg = "black", fg = "white" ,font=("Courier New", 70),text="OBOMBA")
        title.grid(row=1,column=1)
        begin = tkinter.Button(self,text="BEGIN",font=("Courier New", 10),command = self.password)
        begin.grid(row=3,column=1)
        self.img = PhotoImage(file="flag.png")
        self.img = self.img.subsample(7,7)
        self.image1 = Label(self,bg="black", image=self.img)
        self.image1.grid(row = 1, column = 0, rowspan=2)
        self.image2 = Label(self,bg="black", image=self.img)
        self.image2.grid(row = 1, column = 2, rowspan=2)
        self.pack(fill=BOTH, expand=True)
    
    def password(self):
        self.phase=1
        self.erase()
        label = Label(self,bg = "black", fg = "white" ,font=("Courier New", 20), text='Password:')
        label.pack()
        
        label.after(1000, setup_phases)
        self.start_password = Label(self,bg = "black", fg="lawn green",font=("Courier New", 70), text="")
        self.start_password.pack()
        begin = tkinter.Button(self,text="BEGIN",command = self.setupBoot)
        begin.pack()
        self.pack(fill=BOTH, expand=True)
    
    # sets up the LCD "boot" GUI
    def setupBoot(self):
        self.erase()
        self.phases = 2
        # set column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        # the scrolling informative "boot" text
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 14), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)
        self.pack(fill=BOTH, expand=True)
        bootup()
        

    # sets up the LCD GUI
    def setup(self):
        
        # the timer
        self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
        self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        # the keypad passphrase
        self._lkeypad = Label(self, bg="black", fg="#ff0000", font=("Courier New", 18), text="Keypad phase: ")
        self._lkeypad.grid(row=2, column=0, columnspan=3, sticky=W)
        # the jumper wires status
        self._lwires = Label(self, bg="black", fg="#ff0000", font=("Courier New", 18), text="Wires phase: ")
        self._lwires.grid(row=3, column=0, columnspan=3, sticky=W)
        # the pushbutton status
        self._lbutton = Label(self, bg="black", fg="#ff0000", font=("Courier New", 18), text="Button phase: ")
        self._lbutton.grid(row=4, column=0, columnspan=3, sticky=W)
        # the toggle switches status
        self._ltoggles = Label(self, bg="black", fg="#ff0000", font=("Courier New", 18), text="Toggles phase: ")
        self._ltoggles.grid(row=5, column=0, columnspan=2, sticky=W)
        # the strikes left
        self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
        self._lstrikes.grid(row=5, column=2, sticky=W)
        
        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._bpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Pause", anchor=CENTER, command=self.pause)
            self._bpause.grid(row=6, column=0, pady=40)
            
            self.wire = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Wire", anchor=CENTER, command=self.obamaDisplay)
            self.wire.grid(row=6, column=1, pady=40)
            # the quit button
            self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
            self._bquit.grid(row=6, column=2, pady=40)
            
    def obamaDisplay(self):
        self.erase()
        self.phase = 3
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)
        self.img = PhotoImage(file="Obama.png")
        self.img = self.img.subsample(3,3)
        self.image = Label(self,bg="black", image=self.img)
        self.image.grid(row=0,column=0,rowspan=5)
        self.spass = Label(self, bg="black", fg="white",font=("Courier New", 20),text = "Secret Password:")
        self.spass.grid(row=0,column=1)
        self.r = tkinter.Button(self, bg="red", fg="white",font=("Courier New", 20),text = "Riddle", command = self.riddle)
        self.r.grid(row=1,column=2)
        
    def riddle(self):
        self.riddle = [q1, q2,q3,q4,q5,q6,q7,q8,q9,q10]
        q1 = Question("What is the capital of France?", ["Berlin", "Paris", "London", "Madrid"], "Paris")
        q2 = Question("Which planet is the fourth going from the sun?", ["Mars", "Earth", "Venus", "Jupiter"], "Mars")
        q3 = Question("What is the largest mammal?", ["Elephant", "Blue Whale ", "Giraffe", "Hippopotamus"], "Blue Whale")
        q4 = Question("Which one of these presidents wasn't shot in office?", ["Adams", "Lincoln", "Roosevelt", "Garfield"], "Adams")
        q5 = Question("Choose one of the following doors, only one can you survive", [" A bear that just ate cocaine", " Three velociraptor that hasn't eaten in three days", "Batman with a killing rule"], "A tiger that hasn't eaten in five weeks")
        q6 = Question(" What is the capital of Russia?", [ "St.Petersburg","Berlin","Kursk"], " Moscow")
        q7 = Question(" How many offical sports teams does University of Tampa have?", ["17", "20", "26", "13"], "20")
        q8 = Question(" University of Tampa as of now has what percentage acceptance rate ?", ["48%",  "56%", "58%"], "54%")
        q9 = Question( " Which of these presidents was seventh US president?", [" Theodore Roosevelt", " Andrew Jackson ", "Abraham Lincoln", " Henry Ford"], "Andrew Jackson")
        q10 = Question(" If I gave you the binary represensation of 00101001 what is the value ?", [ " 36", "56", "48"], "41")

        
        
        FRA= []
        temp = toggles
       
        if (temp - 8)!=0:
            FRA.append(random.choice(q1,q7,q3))
            temp -= 8
        if (temp -4)!=0:
            FRA.append(random.choice(q2,q4))
            temp -= 4
        if (temp - 2) != 0:
            FRA.append(random.choice(q6,q7))
            temp -= 2 
        if (temp -1) !=0:
            FRA.appeand(random.choice(q8, q9,))
        
         
        
        
        
        color = ["red","white","blue"]
        self.box = Label(self,bg=rng.choice(color), fg="black",font=("Courier New", 20),text = self.riddle)
        self.box.grid(row=3, column= 1, rowspan = 5, columnspan=2)
        

        
    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button

    # pauses the timer
    def pause(self):
        if (RPi):
            self._timer.pause()

    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, exploding=False, success=False):
        while (not exploding and pygame.mixer.music.get_busy()):
            sleep(0.1)
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._lstrikes.destroy()
        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bquit.destroy()
        self.erase()

        # reconfigure the GUI
        # the appropriate (success/explode) image
        if (success):
            image = PhotoImage(file=SUCCESS[0])
        else:
            image = PhotoImage(file=EXPLODE[0])
        self._lscroll["image"] = image
        self._lscroll.image = image
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=EW)
        # the retry button
        self._bretry = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Retry", anchor=CENTER, command=self.retry)
        self._bretry.grid(row=1, column=0, pady=40)
        # the quit button
        self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
        self._bquit.grid(row=1, column=2, pady=40)
        # play the appropriate (success/explode) audio
        if (success):
            pygame.mixer.music.load(SUCCESS[1])
        else:
            pygame.mixer.music.load(EXPLODE[1])
        pygame.mixer.music.play(1)

    # re-attempts the bomb (after an explosion or a successful defusion)
    def retry(self):
        # re-launch the program (and exit this one)
        os.execv(sys.executable, ["python3"] + [sys.argv[0]])
        exit(0)

    # quits the GUI, resetting some components
    def quit(self):
        if (RPi):
            # turn off the 7-segment display
            self._timer._running = False
            self._timer._component.blink_rate = 0
            self._timer._component.fill(0)
            # turn off the pushbutton's LED
            for pin in self._button._rgb:
                pin.value = True
        # exit the application
        exit(0)

# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        # phases have an electronic component (which usually represents the GPIO pins)
        self._component = component
        # phases have a target value (e.g., a specific combination on the keypad, the proper jumper wires to "cut", etc)
        self._target = target
        # phases can be successfully defused
        self._defused = False
        # phases can be failed (which result in a strike)
        self._failed = False
        # phases have a value (e.g., a pushbutton can be True/Pressed or False/Released, several jumper wires can be "cut"/False, etc)
        self._value = None
        # phase threads are either running or not
        self._running = False

# template (superclass) for various numeric bomb components/phases
# these types of phases can be represented as the binary representation of an integer
# e.g., jumper wires phase, toggle switches phase
class NumericPhase(PhaseThread):
    def __init__(self, name, component=None, target=None, display_length=0):
        super().__init__(name, component, target)
        # the default value is the current state of the component
        self._value = self._get_int_state()
        # we need to know the previous state to detect state change
        self._prev_value = self._value
        # we need to know the display length (character width) of the pin states (for the GUI)
        self._display_length = display_length

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # get the component value
            self._value = self._get_int_state()
            # the component value is correct -> phase defused
            if (self._value == self._target):
                self._defused = True
            # the component state has changed
            elif (self._value != self._prev_value):
                # one or more component states are incorrect -> phase failed (strike)
                if (not self._check_state()):
                    self._failed = True
                # note the updated state
                self._prev_value = self._value
            sleep(0.1)

    # checks the component for an incorrect state (only internally called)
    def _check_state(self):
        # get a list (True/False) of the current, previous, and valid (target) component states
        states = self._get_bool_state()
        prev_states = [ bool(int(c)) for c in bin(self._prev_value)[2:].zfill(self._display_length) ]
        valid_states = [ bool(int(c)) for c in bin(self._target)[2:].zfill(self._display_length) ]
        # go through each component state
        for i in range(len(states)):
            # a component state has changed *and* it is in an invalid state -> phase failed (strike)
            if (states[i] != prev_states[i] and states[i] != valid_states[i]):
                return False
        return True

    # returns the state of the component as a list (True/False)
    def _get_bool_state(self):
        return [ pin.value for pin in self._component ]

    # returns the state of the component as an integer
    def _get_int_state(self):
        return int("".join([ str(int(n)) for n in self._get_bool_state() ]), 2)

    # returns the state of the component as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return f"{bin(self._value)[2:].zfill(self._display_length)}/{self._value}"

# the timer phase
class Timer(PhaseThread):
    def __init__(self, component, initial_value, name="Timer"):
        super().__init__(name, component)
        # the default value is the specified initial value
        self._value = initial_value
        # is the timer paused?
        self._paused = False
        # initialize the timer's minutes/seconds representation
        self._min = ""
        self._sec = ""
        # by default, each tick is 1 second
        self._interval = 1

    # runs the thread
    def run(self):
        self._running = True
        count = 0 
        while (self._running):

            if (not self._paused):
                if self._value % 2:
                    c = ["R","B","G"]
                    
                    button.color = c[count]
                    count +=1
                    if count == 3:
                        count = 0
                
                # update the timer and display its value on the 7-segment display
                self._update()
                self._component.print(str(self))
                # wait 1s (default) and continue
                sleep(self._interval)
                # the timer has expired -> phase failed (explode)
                if (self._value == 0):
                    self._running = False
                self._value -= 1
            else:
                sleep(0.1)

    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)

    # pauses and unpauses the timer
    def pause(self):
        # toggle the paused state
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._component.blink_rate = (2 if self._paused else 0)

    # returns the timer as a string (mm:ss)
    def __str__(self):
        return f"{self._min}:{self._sec}"

# the keypad phase
class Keypad(PhaseThread):
    def __init__(self, component, target, name="Keypad"):
        super().__init__(name, component, target)
        # the default value is an empty string
        self._value = ""

    # runs the thread
    def run(self):
        self._running = True
        cracked = False
        while (self._running):
            # process keys when keypad key(s) are pressed
            if (self._component.pressed_keys):
                # debounce
                while (self._component.pressed_keys):
                    try:
                        # just grab the first key pressed if more than one were pressed
                        key = self._component.pressed_keys[0]
                    except:
                        key = ""
                    sleep(0.1)
                # log the key
                self._value += str(key)
                
                # the combination is correct -> phase defused
                if gui.phase == 1 and cracked == False:
                    target = "62262"
                    if key == "#":
                        gui.start_password.configure(text = f"{self._value}")
                        if (self._value == "62262#"):
                            gui.setupBoot()
                            cracked = True
                            self._value == ""
                        self._value = ""
                        
                    else:
                        gui.start_password.configure(text = f"{self._value}")
                    
                        '''
                    # the combination is incorrect -> phase failed (strike)
                    elif (self._value != target[0:len(self._value)]):
                        self._failed = True
                        '''
                    sleep(0.1)
                    

    # returns the keypad combination as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return self._value

# the jumper wires phase
class Wires(NumericPhase):
    def __init__(self, component, target, display_length, name="Wires"):
        super().__init__(name, component, target, display_length)
    
    def run(self):
        self._running = True
        while (self._running):
            # get the component value
            self._value = self._get_int_state()
            # the component value is correct -> phase defused
            if gui.phase == 2:
                if (self._value == self._target):
                    gui.obamaDisplay()
            # the component state has changed
            if (self._value != self._prev_value):
                # one or more component states are incorrect -> phase failed (strike)
                if (not self._check_state()):
                    self._failed = True
                # note the updated state
                self._prev_value = self._value
            sleep(0.1)
    # returns the jumper wires state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return "".join([ chr(int(i)+65) if pin.value else "." for i, pin in enumerate(self._component) ])

# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, target, color, timer, name="Button"):
        super().__init__(name, component_state, target)
        # the default value is False/Released
        self._value = False
        # has the pushbutton been pressed?
        self._pressed = False
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        # the pushbutton's randomly selected LED color
        self.color = color
        
        # we need to know about the timer (7-segment display) to be able to determine correct pushbutton releases in some cases
        self._timer = timer
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, c):
        self._color = c
    
    # runs the thread
    def run(self):
        start = 0
        end = 0 
        self._running = True
        p = ''
        password = 'michelleobama'
        q = Queue()
        for i in password:
            q.enqueue(i)
        # set the RGB LED color
        
        while (self._running):
            self._rgb[0].value = False if self.color == "R" else True
            self._rgb[1].value = False if self.color == "G" else True
            self._rgb[2].value = False if self.color == "B" else True
            # get the pushbutton's state
            self._value = self._component.value
            # it is pressed
            if gui.phase == 3:
                if end-start >= 2:
                    gui.riddle()
                    start =0
                    end = 0
            if (self._value):
                if self._pressed == False:
                    start = time.time()
                self._pressed = True
            
            # it is released
            else:
                # was it previously pressed?
                if (self._pressed):
                    end = time.time()
                    # check the release parameters
                    # for R, nothing else is needed
                    # for G or B, a specific digit must be in the timer (sec) when released
                    if (not self._target or self._target in self._timer._sec) and self.color == 'B':
                        p = p + q.dequeue()
                        gui.spass.configure(text = f"Secret Password:\n {p}")
                    else:
                        self._failed = True
                    # note that the pushbutton was released
                    self._pressed = False
                    
            sleep(0.1)

    # returns the pushbutton's state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return str("Pressed" if self._value else "Released")

# the toggle switches phase
class Toggles(NumericPhase):
    def __init__(self, component, target, display_length, name="Toggles"):
        super().__init__(name, component, target, display_length)
###########
# functions
###########
# generates the bootup sequence on the LCD
def bootup(n=0):
    # if we're not animating (or we're at the end of the bootup text)
    if (not ANIMATE or n == len(boot_text)):
        # if we're not animating, render the entire text at once (and don't process \x00)
        if (not ANIMATE):
            gui._lscroll["text"] = boot_text.replace("\x00", "")
        # configure the remaining GUI widgets
        gui.setup()
        # setup the phase threads, execute them, and check their statuses
        
    # if we're animating
    else:
        # add the next character (but don't render \x00 since it specifies a longer pause)
        if (boot_text[n] != "\x00"):
            gui._lscroll["text"] += boot_text[n]

        # scroll the next character after a slight delay (\x00 is a longer delay)
        gui.after(25 if boot_text[n] != "\x00" else 750, bootup, n + 1)

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
        if gui.phase == 2:
            # play the exploding audio at t-10s
            if (not exploding and timer._interval * timer._value <= 11.25):
                exploding = True
                component_7seg.blink_rate = 1
                pygame.mixer.music.load(EXPLODING)
                pygame.mixer.music.play(1)
            
            gui._ltimer["text"] = f"Time left: {timer}"
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
        if gui.phase == 2:
            gui.start_password.configure(text = f"{keypad}")
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
        if gui.phase == 2:
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
        if gui.phase == 2:
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
        if gui.phase == 2:
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
    if gui.phase == 2:
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
gui = Lcd(window)


# initialize the bomb strikes, active phases (i.e., not yet defused), and if the bomb is exploding
strikes_left = NUM_STRIKES
active_phases = NUM_PHASES
exploding = False

# "boot" the bomb



# display the LCD GUI
window.mainloop()
