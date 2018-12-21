from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from subprocess import Popen, PIPE
import time
import subprocess

#import wiringpi as wpi

#Create global variables to avoid passing them
global LeftFront
global RightFront
global LeftRear
global RightRear

LeftFront = 0
RightFront = 0
LeftRear = 0
RightRear = 0

#Kivy code for GUI
Builder.load_string('''

#Create the main screen layout
<MainScreen>:
    
    #MainScreen background
    Image:
        source: 'orig.jpg'
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        allow_stretch: True
        keep_ratio: False    
    Label:
        text: 'Acura Suspension Control'
        font_size: '20sp'
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        color: [1,0,0,1]
    FloatLayout:
        id: MainScree

    #Create buttons for main screen      
    Button:
        text: '>'
        id: FRS
        size_hint: None, None
        pos_hint: {'center_x': 0.25, 'center_y': 0.9}
        size_hint: .05, .1
        on_press: root.FRS()
    Button:
        text: '<'
        id: FRT
        size_hint: None, None
        pos_hint: {'center_x': 0.2, 'center_y': 0.9}
        size_hint: .05, .1
        on_press: root.FRT() 
    Button:
        text: '<'
        id: RRT
        size_hint: None, None
        pos_hint: {'center_x': 0.75, 'center_y': 0.9}
        size_hint: .05, .1
        on_press: root.RRT()
    Button:
        text: '>'
        id: RRS
        size_hint: None, None
        pos_hint: {'center_x': 0.8, 'center_y': 0.9}
        size_hint: .05, .1
        on_press: root.RRS()
    Button:
        text: '<'
        id: FLT
        size_hint: None, None
        pos_hint: {'center_x': 0.2, 'center_y': 0.1}
        size_hint: .05, .1
        on_press: root.FLT()
    Button:
        text: '>'
        id: FLS
        size_hint: None, None
        pos_hint: {'center_x': 0.25, 'center_y': 0.1}
        size_hint: .05, .1
        on_press: root.FLS()
    Button:
        text: '<'
        id: RLT
        size_hint: None, None
        pos_hint: {'center_x': 0.75, 'center_y': 0.1}
        size_hint: .05, .1
        on_press: root.RLT()
    Button:
        text: '>'
        id: RLS
        size_hint: None, None
        pos_hint: {'center_x': 0.8, 'center_y': 0.1}
        size_hint: .05, .1
        on_press: root.RLS()
    Button:
        text: '<'
        id: REART
        size_hint: None, None
        pos_hint: {'center_x': 0.9, 'center_y': 0.55}
        size_hint: .05, .1
        on_press: root.REART()
    Button:
        text: '>'
        id: REARS
        size_hint: None, None
        pos_hint: {'center_x': 0.95, 'center_y': 0.55}
        size_hint: .05, .1
        on_press: root.REARS()
    Button:
        text: '<'
        id: FRONTT
        size_hint: None, None
        pos_hint: {'center_x': 0.05, 'center_y': 0.55}
        size_hint: .05, .1
        on_press: root.FRONTT()
    Button:
        text: '>'
        id: FRONTS
        size_hint: None, None
        pos_hint: {'center_x': 0.1, 'center_y': 0.55}
        size_hint: .05, .1
        on_press: root.FRONTS()
    Button:
        text: '<'
        id: ALLT
        size_hint: None, None
        pos_hint: {'center_x': 0.6, 'center_y': 0.55}
        size_hint: .05, .1
        on_press: root.ALLT()
    Button:
        text: '>'
        id: ALLS
        size_hint: None, None
        pos_hint: {'center_x': 0.65, 'center_y': 0.55}
        size_hint: .05, .1
        on_press: root.ALLS()
    Button:
        text: 'Presets'
        id: Presets
        size_hint: None, None
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        size_hint: .3, .1
        on_release:
            root.manager.current = 'PresetScreen'
            root.manager.transition.direction = 'right'

#Create layout for preset button screen
<PreScreen>:
    hue: random()
    Image:
        source: 'orig.jpg'
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        allow_stretch: True
        keep_ratio: False
    GridLayout:
        id: PresetAnchor
        cols: 4
        rows: 3
        padding: [60, 60, 60, 60]
        row_default_hieght: 200
    Button:
        text: 'Back'
        id: Back
        size_hint: None, None
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        size_hint: .3, .1
        on_release:
            root.manager.current = 'Main'
            root.manager.transition.direction = 'left'

''')

#Main App Screen
class MainScreen(Screen):

    #Global variables are bad, mkay
    global LeftFront
    global RightFront
    global LeftRear
    global RightRear

    #Removed rx because 3.3v to 5v serial is problematic
    #Need to convert between voltages physically 
    #serial = wpi.serialOpen('/dev/ttyS0', 9600)
    #settings = 'settings'
    #while wpi.serialDataAvail(serial):
        #settings += chr(wpi.serialGetchar(serial))

# Create buttons and labels when entering main screen
    def on_enter(self):
        try:

            #Set up serial
            subprocess.call(["su -c 'stty -F /dev/ttyS1 115200'"], shell=True)

            #Create labels for settings
            self.Setting1 = Label(text= str(LeftFront), pos_hint={'center_x':0.2, 'center_y':0.18}, color=[1,0,0,1])
            self.Setting2 = Label(text= str(RightFront), pos_hint={'center_x':0.2, 'center_y':0.98},color=[1,0,0,1] )
            self.Setting3 = Label(text= str(LeftRear), pos_hint={'center_x':0.8, 'center_y':0.18}, color=[1,0,0,1])
            self.Setting4 = Label(text= str(RightRear), pos_hint={'center_x':0.8, 'center_y':0.98},color=[1,0,0,1] )
        
            #Add labels to screen
            self.ids.MainScree.add_widget(self.Setting1)
            self.ids.MainScree.add_widget(self.Setting2)
            self.ids.MainScree.add_widget(self.Setting3)
            self.ids.MainScree.add_widget(self.Setting4)
        except:
            pass

    #Clear widgets on leave
    def on_leave(self):
        self.ids.MainScree.clear_widgets()

    #Update screen on each touch event
    def on_touch_up(self, touch):
        self.ids.MainScree.clear_widgets()
        self.Setting1 = Label(text= str(LeftFront), pos_hint={'center_x':0.2, 'center_y':0.18}, color=[1,0,0,1])
        self.Setting2 = Label(text= str(RightFront), pos_hint={'center_x':0.2, 'center_y':0.98},color=[1,0,0,1] )
        self.Setting3 = Label(text= str(LeftRear), pos_hint={'center_x':0.8, 'center_y':0.18}, color=[1,0,0,1])
        self.Setting4 = Label(text= str(RightRear), pos_hint={'center_x':0.8, 'center_y':0.98},color=[1,0,0,1] )
        
        self.ids.MainScree.add_widget(self.Setting1)
        self.ids.MainScree.add_widget(self.Setting2)
        self.ids.MainScree.add_widget(self.Setting3)
        self.ids.MainScree.add_widget(self.Setting4)
        pass
     
    #Individual buttons for control
    def FRS(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            subprocess.call(["su -c 'echo 21 > /dev/ttyS1'"], shell=True)
            if(RightFront<100):
                RightFront=RightFront +1
        except:
            pass
        pass
    def FRT(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            subprocess.call(["su -c 'echo 22 > /dev/ttyS1'"], shell=True)
            if(RightFront>0):
                RightFront=RightFront-1
        except:
            pass
        pass
    
    def FLS(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            subprocess.call(["su -c 'echo 11 > /dev/ttyS1'"], shell=True)
            if(LeftFront<100):
                LeftFront=LeftFront+1
        except:
            pass
        pass
    def FLT(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            subprocess.call(["su -c 'echo 12 > /dev/ttyS1'"], shell=True)
            if(LeftFront>0):
                LeftFront=LeftFront-1
        except:
            pass
        pass
    
    def RRS(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            subprocess.call(["su -c 'echo 41 > /dev/ttyS1'"], shell=True)
            if(RightRear<100):
                RightRear=RightRear+1
        except:
            pass
        pass
    def RRT(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            subprocess.call(["su -c 'echo 42 > /dev/ttyS1'"], shell=True)
            if(RightRear>0):
                RightRear=RightRear-1
        except:
            pass
        pass
    
    def RLS(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            subprocess.call(["su -c 'echo 31 > /dev/ttyS1'"], shell=True)
            if(LeftRear<100):
                LeftRear=LeftRear+1
        except:
            pass
        pass
    def RLT(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            subprocess.call(["su -c 'echo 32 > /dev/ttyS1'"], shell=True)
            if(LeftRear>0):
                LeftRear=LeftRear-1
        except:
            pass
        pass

# Front and rear control
    def FRONTS(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            if(RightFront<100 and LeftFront<100):
                subprocess.call(["su -c 'echo 51 > /dev/ttyS1'"], shell=True)
                RightFront=RightFront+1
                LeftFront=LeftFront+1
        except:
            pass
        pass
    def FRONTT(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            if(RightFront>0 and LeftFront>0):
                subprocess.call(["su -c 'echo 52 > /dev/ttyS1'"], shell=True)
                RightFront=RightFront-1
                LeftFront=LeftFront-1
        except:
            pass
        pass

    def REARS(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            if(RightRear<100 and LeftRear<100):
                subprocess.call(["su -c 'echo 61 > /dev/ttyS1'"], shell=True)
                RightRear=RightRear+1
                LeftRear=LeftRear+1
        except:
            pass
        pass
    def REART(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            if(RightRear>0 and LeftRear>0):
                subprocess.call(["su -c 'echo 62 > /dev/ttyS1'"], shell=True)
                RightRear=RightRear-1
                LeftRear=LeftRear-1
        except:
            pass
        pass

# All corner control

    def ALLS(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            if(RightFront<100 and LeftFront<100 and RightRear<100 and LeftRear<100):
                subprocess.call(["su -c 'echo 71 > /dev/ttyS1'"], shell=True)
                RightFront=RightFront+1
                LeftFront=LeftFront+1
                RightRear=RightRear+1
                LeftRear=LeftRear+1
        except:
            pass
        pass
    def ALLT(self):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        try:
            if(RightFront>0 and LeftFront>0 and RightRear>0 and LeftRear>0):
                subprocess.call(["su -c 'echo 72 > /dev/ttyS1'"], shell=True)
                RightFront=RightFront-1
                LeftFront=LeftFront-1
                RightRear=RightRear-1
                LeftRear=LeftRear-1
        except:
            pass
        pass

#This is the preset screen class
#It uses preset values to change settings
class PreScreen(Screen):
    global LeftFront
    global RightFront
    global LeftRear
    global RightRear

    #When entering screen, create buttons
    def on_enter(self):
        self.tgl1 = ToggleButton(text='Comfort', group='Preset', size_hint_y=None, height=100)
        self.tgl1.bind(on_press=self.Comfort)
        self.tgl2 = ToggleButton(text='Normal', group='Preset', size_hint_y=None, height=100)
        self.tgl2.bind(on_press=self.Normal)
        self.tgl3 = ToggleButton(text='Sport', group='Preset', size_hint_y=None, height=100, on_state=self.Sport)
        self.tgl3.bind(on_press=self.Sport)
        self.tgl8 = ToggleButton(text='Custom', group='Preset', size_hint_y=None, height=100)

        self.tgl4 = ToggleButton(text='Oversteer', group='Steering', size_hint_y=None, height=100)
        self.tgl5 = ToggleButton(text='Balanced', group='Steering', size_hint_y=None, height=100)
        self.tgl6 = ToggleButton(text='Understeer', group='Steering', size_hint_y=None, height=100)
        self.tgl7 = ToggleButton(text='Custom', group='Steering', size_hint_y=None, height=100)
        
        self.ids.PresetAnchor.add_widget(self.tgl1)
        self.ids.PresetAnchor.add_widget(self.tgl2)
        self.ids.PresetAnchor.add_widget(self.tgl3)
        self.ids.PresetAnchor.add_widget(self.tgl8)

        self.ids.PresetAnchor.add_widget(self.tgl4)
        self.ids.PresetAnchor.add_widget(self.tgl5)
        self.ids.PresetAnchor.add_widget(self.tgl6)
        self.ids.PresetAnchor.add_widget(self.tgl7)

    #Clear the screen of messeges when leaving
    def on_leave (self):
        self.ids.PresetAnchor.clear_widgets()

    #Create comfort setting
    def Comfort(self, touch):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        LeftFront=60
        RightFront=60
        LeftRear=60
        RightRear=60
        try:
            subprocess.call(["su -c 'echo 15 > /dev/ttyS1'"], shell=True)
            LeftFront=Set
        except:
            pass
    #Create normal mode
    def Normal(self, touch):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        LeftFront=20
        RightFront=20
        LeftRear=20
        RightRear=20
        try:
            subprocess.call(["su -c 'echo 14 > /dev/ttyS1'"], shell=True)
            LeftFront=Set
        except:
            pass

    #Create sport mode
    def Sport(self, touch):
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        LeftFront=5
        RightFront=5
        LeftRear=5
        RightRear=5
        try:
            subprocess.call(["su -c 'echo 13 > /dev/ttyS1'"], shell=True)
            LeftFront=Set
        except:
            pass
'''   
    #Allow prsets to change- not implemented/incomplete
    def ChangePreset(self, Set):
        print(Set)
        global LeftFront
        global RightFront
        global LeftRear
        global RightRear
        if (LeftFront<Set):
            Temp1=Set-LeftFront
            for i in range(0, Temp1):
                try:
                    subprocess.call(["su -c 'echo 11 > /dev/ttyS1'"], shell=True)
                    LeftFront=Set
                except:
                    pass
        if(LeftFront>Set):
            Temp1=LeftFront-Set
            for i in range(0, Temp1):
                try:
                    subprocess.call(["su -c 'echo 12 > /dev/ttyS1'"], shell=True)
                    LeftFront=Set
                except:
                    pass
        if(RightFront<Set):
            Temp1=Set-RightFront
            for i in range(0, Temp1):
                try:
                    subprocess.call(["su -c 'echo 21 > /dev/ttyS1'"], shell=True)
                    RightFront=Set
                except:
                    pass
        if(RightFront>Set):
            Temp1=RightFront-Set
            for i in range(0, Temp1):
                try:
                    subprocess.call(["su -c 'echo 22 > /dev/ttyS1'"], shell=True)
                    RightFront=Set
                except:
                    pass
        if (LeftRear<Set):
            Temp1=Set-LeftRear
            for i in range(0, Temp1):
                try:
                    subprocess.call(["su -c 'echo 31 > /dev/ttyS1'"], shell=True)
                    LeftRear=Set
                except:
                    pass
        if(LeftRear>Set):
            Temp1=LeftRear-Set
            for i in range(0, Temp1):
                try:
                    subprocess.call(["su -c 'echo 32 > /dev/ttyS1'"], shell=True)
                    LeftRear=Set
                except:
                    pass
        if (RightRear<Set):
            Temp1=Set-RightRear
            for i in range(0, Temp1):
                try:
                    subprocess.call(["su -c 'echo 41 > /dev/ttyS1'"], shell=True)
                    RightRear=Set
                except:
                    pass
        if(RightRear>Set):
            Temp1=RightRear-Set
            for i in range(0, Temp1):
                try:
                    subprocess.call(["su -c 'echo 42 > /dev/ttyS1'"], shell=True)
                    RightRear=Set
                except:
                    pass
'''

#Add the other screens to the screen manager
screen = ScreenManager()
screen.add_widget(MainScreen(name='Main'))
screen.add_widget(PreScreen(name='PresetScreen'))

# Run the app
class AcuraApp(App):
        
    def build(self):
        return screen
    
if __name__ == '__main__':
    AcuraApp().run()
