from kivy.core.window import Window
from kivy.lang import Builder
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.screen import  Screen
from base64 import *
import paramiko
import socket
from kivy.clock import Clock
# aKivymd
from kivymd_extensions.akivymd.uix.charts import AKBarChart, AKPieChart


from kivy_garden.mapview import MapMarker, MapView
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
# high potential for breaking
import requests
from urllib.error import HTTPError

from kivymd.uix.list import IconRightWidget

import io
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
KV = """
# creating the navbar that opens
<ContentNavigationDrawer>:
    ScrollView:
    # list of selections to click from in the navbar
        MDList:
            OneLineListItem:
                text: "Status"
                on_press:
                    # close the navbar and navigate to a new page
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "pg_status"
            
            OneLineListItem:
                text: "Location"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "pg_location"

            OneLineListItem:
                text: "Alerts"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "pg_alerts"

            OneLineListItem:
                text: "Controls"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "pg_controls"

            OneLineListItem:
                text: "Remote Access"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "pg_remote_access"

            OneLineListItem:
                text: "Database"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "pg_db"
            
            OneLineListItem:
                text: "Statistics"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "pg_stats"

                    
# base screen that holds the toolbar and upper banner for all screens, removing this causes errors as it is the base template for all pages
Screen:
    MDToolbar:
        id: toolbar
        padding: 20
        pos_hint: {"top": 1}
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
        MDFloatLayout:
            MDLabel:
                pos_hint: {"x": -0.225, "y": 0} 
                text:""
                text_color: 0, 0, 1, 1

# Holds all the screens that are in the app
    MDNavigationLayout:
        x: toolbar.height
        ScreenManager:
            id: screen_manager
 
            DummyScreen:

            StatusScreen:
            
            LocationScreen:

            AlertsScreen:

            ControlsScreen:

            ScopeScreen:

            RemoteAccessScreen:

            DatabaseScreen:

            StatisticsScreen:

        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer

<DummyScreen>:
    MDIconButton:
        id: left
        icon: "icons/owr.png"
        user_font_size: "100sp"
        pos_hint: {"center_x": .5, "center_y": 0.5}
        pos: (0, 0)
        # on_press: root.turn_left()
        disabled: False
        opacity: 1

# Status Screen  
<StatusScreen>:
    name: "pg_status"
    MDFloatLayout:
        MDLabel:
            id: task_label
            halign: 'center'
            markup: True
            text: "Status"
            font_name: "fonts/Arialn.ttf"
            pos_hint: {"x": 0.02, 'y': .47}
            font_size: '20sp'
            color: 1, 1, 1, 1

        # 1/3 status circular progress widgets (progress_percent0)
        AKCircularProgress:
            id: progress_percent0
            pos_hint: {"x": 0.05, 'y': .7}
            # essential for size maintenance
            size_hint: None, None
            # size of the dial => 75%
            size: dp(75), dp(75)
            # percent allows for valid percentages
            percent_type: "percent"
            # starting from the bottom of the circle and raising from there
            start_deg: 180
            end_deg: 540

        MDLabel:
            # pos: 50, 80
            pos_hint: {"center_x": .59, "center_y": .67}
            text: 'Battery'
            font_name: "fonts/Arialn.ttf"
            
        # 2/3 status circular progress widgets (progress_percent1)
        AKCircularProgress:
            id: progress_percent1
            pos_hint: {"x": 0.375, 'y': .7}
            # essential for size maintenance
            size_hint: None, None
            # size of the dial
            size: dp(75), dp(75)
            percent_type: "percent"
            start_deg: 180
            end_deg: 540
    
        MDLabel:
            # pos: 530, 80
            pos_hint: {"center_x": 0.935, "center_y": .67}
            text: "Load"
            font_name: "fonts/Arialn.ttf"

        # 3/3 status circular progress widgets (progress_percent2) 
        AKCircularProgress:
            id: progress_percent2
            pos_hint: {"x": 0.7, 'y': .7}
            # essential for size maintenance
            size_hint: None, None
            # size of the dial
            size: dp(75), dp(75)
            percent_type: "percent"
            start_deg: 180
            end_deg: 540
    
        MDLabel:
            # pos: 880, 80
            pos_hint: {"center_x": 1.25, "center_y": .67}
            text: "Speed"
            font_name: "fonts/Arialn.ttf"

        MDIconButton:
            id: power_on
            user_font_size: "64sp"
            # pos_hint: {"center_x": .5, "center_y": .3}
            pos :(0, 0)
            on_release: root.power_off()
            disabled: True
            opacity: 0

        MDIconButton:
            id: power_on
            icon: "icons/On.png"
            user_font_size: "64sp"
            # pos_hint: {"center_x": .5, "center_y": .3}
            pos :(0, 0)
            on_release: root.power_off()
            disabled: True
            opacity: 0
        
        MDIconButton:
            id: power_off
            icon: "icons/Off.png"
            user_font_size: "64sp"
            # pos_hint: {"center_x": .5, "center_y": .3}
            pos :(250, 150)
            on_release: root.power_on()
            disabled: False
            opcaity: 1

# labels for Time values
        MDLabel:
            id: remainingTime
            pos: 10, 50
            text: "Remaining Time: "
            font_name: "fonts/Arialn.ttf"

        MDLabel:
            id: sshtest
            pos: 10, 10
            text: "SSH: Testing"


<LocationScreen>:
    name: 'pg_location'
    # map dimensions
    size_hint: 1, 0.93
    height: "435dp"

    # adding label under the OWR label to mark screen
    MDFloatLayout:
        MDLabel:
            id: task_label
            halign: 'center'
            markup: True
            text: "Location"
            font_name: "fonts/Arialn.ttf"
            pos_hint: {"x": 0.04, 'y': 0.54}
            font_size: '20sp'
            color: 1, 1, 1, 1



<AlertsScreen>:
    name: "pg_alerts"    
    # adding label under the OWR label to mark screen     
    MDFloatLayout:
        MDLabel:
            id: task_label
            halign: 'center'
            markup: True
            text: "Alerts"
            font_name: "fonts/Arialn.ttf"
            pos_hint: {"x": 0.02, 'y': .47}
            font_size: '20sp'
            color: 1, 1, 1, 1

        # This sql check label will display pon entering the screen, its text will be replaced when the sql
        MDLabel:
            id: sql_label
            # halign: 'center'
            markup: True
            text: "Checking SQL Database Connection"
            font_name: "fonts/Arialn.ttf"
            pos_hint: {"x": 0.15, 'y': 0.3}

        MDFlatButton:
            id: sql_retry_button
            text: "Retry"
            pos_hint: {"x": 0.05, 'y': 0.65}
            on_press : root.check_connection()
            md_bg_color: 1, 1, 1, 1
            disabled : True
            opacity : 0
        MDLabel:
            id: urlRequest
            markup: True
            text: "URLTEST"
            pos_hint: {"x": 0, 'y': 0}
            font_size : '10sp'

<ControlsScreen>:
    name: "pg_controls"
    MDFloatLayout:
        MDLabel:
            id: task_label
            halign: 'center'
            markup: True
            text: "Controls"
            font_name: "fonts/Arialn.ttf"
            pos_hint: {"x": 0.02, 'y': .47}
            font_size: '20sp'
            color: 1, 1, 1, 1

        MDLabel:
            text: "Automatic reconnect"
            pos_hint:{"center_x": .55, "center_y": 0.7}

        MDSwitch:
            id: sw_1
            pos_hint:{"center_x": .8, "center_y": 0.7}
            width: dp(45)
            on_active: root.switch1(*args)

        MDLabel:
            text: "Object Alerts"
            pos_hint:{"center_x": .55, "center_y": 0.6}

        MDSwitch:
            id: sw_2
            pos_hint:{"center_x": .8, "center_y": .6}
            width: dp(45)
            on_active: root.switch2(*args)

        MDLabel:
            text: "Trash Collection Alerts"
            pos_hint:{"center_x": .55, "center_y": 0.5}
            
        MDSwitch:
            id: sw_3
            pos_hint:{"center_x": .8, "center_y": .5}
            width: dp(45)
            on_active: root.switch3(*args)

        MDLabel:
            text: "Critical Alerts"
            pos_hint:{"center_x": .55, "center_y": 0.4}
        MDSwitch:
            id: sw_4
            pos_hint:{"center_x": 0.8, "center_y": .4}
            width: dp(45)
            on_active: root.switch4(*args)

        MDRectangleFlatButton:
            text: 'Assign Scope'
            pos_hint: {'center_x': 0.55, 'center_y': 0.2}
            on_press: root.manager.current = 'pg_scope'

<ScopeScreen>:
    name: "pg_scope"
    MDFloatLayout:
        MDLabel:
            id: task_label
            halign: 'center'
            markup: True
            text: "OWR Scope"
            font_name: "fonts/Arialn.ttf"
            # text: "[u][size=48][b]Controls[/b][/size][/u]"
            pos_hint: {"x": 0.03, 'y': .47}
            font_size: '20sp'
            color: 1, 1, 1, 1

        MapViewClass:

<MapViewClass>:
    id: mapview
    size_hint: 1,0.93
    lat: 45.49905745304462
    lon: -73.57308916773897
    zoom: 13
    on_zoom:
        self.zoom = 10 if self.zoom < 10 else self.zoom

    MapMarker:
        id: marker_pointer
        lat : root.lat
        lon : root.lon
        source: "icons/marker.png"

    MapMarker:
        id: marker_pointer
        lat :
        lon :
        source: "icons/marker.png"
    
    MapMarker:
        id: marker_1
        lat : 
        lon :
        source: "icons/marker.png"
    MapMarker:
        id: marker_2
        lat : 
        lon :
        source: "icons/marker.png"
    MapMarker:
        id: marker_3
        lat : 
        lon :
        source: "icons/marker.png"
    MapMarker:
        id: marker_4
        lat : 
        lon :
        source: "icons/marker.png"
    
    Button:
        id: assign_marker_1
        text: "Assign 1"
        size: 350, 120
        pos : (0, 0)
        opacity: 1
        disabled: False
        on_release:
            root.add_marker1()
    Button:
        id: assign_marker_2
        text: "Assign 2"
        size: 350, 120
        pos : (40, 60)
        opacity: 0
        disabled: True
        on_release:
            root.add_marker2()
    Button:
        id: assign_marker_3
        text: "Assign 3"
        size: 350, 120
        pos : (50, 60)
        opacity: 0
        disabled: True
        on_release:
            root.add_marker3()
    Button:
        id: assign_marker_4
        text: "Assign 4"
        size: 350, 120
        pos : (60, 60)
        opacity: 0
        disabled: True
        on_release:
            root.add_marker4()
    
    Button:
        id: remove_markers
        text:"Remove Markers"
        size: 350, 120
        pos :(70, 60)
        opacity: 0
        disabled: True
        on_release:
            root.remove_markers()

<RemoteAccessScreen>:
    name: "pg_remote_access"
    MDFloatLayout:
        MDLabel:
            id: task_label
            halign: 'center'
            markup: True
            text: "Remote Access"
            font_name: "fonts/Arialn.ttf"
            pos_hint: {"x": 0.03, 'y': .47}
            font_size: '20sp'
            color: 1, 1, 1, 1
    
        #downward - left arrow
        MDIconButton:
            id: downward
            icon: "icons/Arrow_Downward.png"
            user_font_size: "32sp"
            pos_hint: {"center_x": .125, "center_y": .2}
            # pos: (0, 0)
            on_press: root.backward()
            disabled: False
            opacity: 1
        
      
        # left - upward arrow
        MDIconButton:
            id: left
            icon: "icons/Arrow_Left.png"
            user_font_size: "32sp"
            pos_hint: {"center_x": .325, "center_y": 0.325}
            # pos: (0, 0)
            on_press: root.turn_left()
            disabled: False
            opacity: 1
    
        
        # right - downward arrow
        MDIconButton:
            id: right
            icon: "icons/Arrow_Right.png"
            user_font_size: "32sp"
            pos_hint: {"center_x": .325, "center_y": 0.075}
            # pos: (0, 0)
            on_press: root.turn_right()
            disabled: False
            opacity: 1
        
          #upward - right arrow
        MDIconButton:
            id: upward
            icon: "icons/Arrow_Upward.png"
            user_font_size: "32sp"
            pos_hint: {"center_x": .525, "center_y": .2}
            # pos: (0, 0)
            on_press: root.forward()
            disabled: False
            opacity: 1

<DatabaseScreen>:
    name: "pg_db"
    on_leave: 
        root.ids.container.clear_widgets()
    MDFloatLayout:
        
        MDLabel:
            id: task_label
            halign: 'center'
            markup: True
            text: "Database"
            font_name: "fonts/Arialn.ttf"
            pos_hint: {"x": 0.03, 'y': .47}
            font_size: '20sp'
            color: 1, 1, 1, 1
            
        ScrollView:
            pos_hint: {"x": 0, 'y': -0.1}
            do_scroll_y: True
            MDGridLayout:
                id: container
                cols: 2
                row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
                row_force_default: True
                adaptive_height: True
                # padding: dp(-5), dp(-5)
                # spacing: dp(1)

            
        # sql checking label and switch
        MDLabel:
            id: sql_label
            # halign: 'center'
            markup: True
            text: "Checking SQL Database Connection"
            font_name: "fonts/Arialn.ttf"
            pos_hint: {"x": 0.15, 'y': 0.3}

        MDFlatButton:
            id: sql_retry_button
            text:"Retry"
            pos_hint: {"x": 0.05, 'y': 0.65}
            on_press : root.check_connection()
            md_bg_color: 1, 1, 1, 1
            disabled : True
            opacity : 0

<StatisticsScreen>
    name: "pg_stats"
    
    MDFloatLayout:
        MDLabel:
            id: task_label
            halign: 'center'
            markup: True
            text: "Statistics"
            pos_hint: {"x": 0.02, 'y': .47}
            font_size: '20sp'
            color: 1, 1, 1, 1

# Bar chart
        MDLabel:
            id: sql_label
            # halign: 'center'
            markup: True
            text: "Checking SQL Database Connection"
            pos_hint: {"x": 0.15, 'y': 0.3}

        MDFlatButton:
            id: sql_retry_button
            text:"Retry"
            pos_hint: {"x": 0.05, 'y': 0.65}
            on_press : root.check_connection()
            md_bg_color: 1, 1, 1, 1
            
            background_color : (1, 1, 1, 1)
            disabled : True
            opacity : 0

            MDLabel:
                id: _label
                halign: "center"
                valign: "center"

# Pie chart
        MDBoxLayout:
            id: chart_box
            orientation: "vertical"
            markup: True
            pos_hint:{"x": 0.055, "y": 0.35}

        MDBoxLayout:
            id: chart_box2
            orientation: "vertical"
            pos_hint:{"x": 0.525, "y": 0.35}
        
        # Database text
        # MDBoxLayout:
        MDLabel:
            markup: True
            text: "Database"
            pos_hint: {"x": 0.4, 'y': 0.1}

        MDLabel:
            markup: True
            text: "Collection"
            pos_hint: {"x": 0.1, 'y': -0.183}
            font_size : '10sp'
        Image:
            pos_hint: {"x": -0.42, 'y': -0.183}
            source: 'icons/circle-blue.png'
            size: 5,5

        MDLabel:
            markup: True
            text: "Pos ID"
            pos_hint: {"x": 0.325, 'y': -0.183}
            font_size : '10sp'
        Image:
            pos_hint: {"x": -0.197, 'y': -0.183}
            source: 'icons/circle-purple.png'
            size: 5,5

        MDLabel:
            markup: True
            text: "Neg ID"
            pos_hint: {"x": 0.5, 'y': -0.183}
            font_size : '10sp'
        Image:
            pos_hint: {"x": -0.02, 'y': -0.183}
            source: 'icons/circle-lightpurple.png'
            size: 2,2
        
        MDLabel:
            markup: True
            text: "Wrong"
            pos_hint: {"x": 0.675, 'y': -0.183}
            font_size : '10sp'
        Image:
            pos_hint: {"x": 0.16, 'y': -0.183}
            source: 'icons/circle-red.png'
            size: 3,3
            
        MDLabel:
            markup: True
            text: "Missed"
            pos_hint: {"x": 0.85, 'y': -0.183}
            font_size : '10sp'
        Image:
            pos_hint: {"x": 0.33, 'y': -0.183}
            source: 'icons/circle-orange.png'
            size: 4,4
                           
"""

class MainApp(MDApp):
    def build(self):
        # self.transition = NoTransition()
        global ssh_hostname
        # ssh_hostname = '10.0.0.22'
        ssh_hostname = '192.168.0.32'
        global ssh_username
        ssh_username = 'jetbot'
        global ssh_password
        ssh_password = 'jetbot'
        global scopexx
        global scopeyy
        return Builder.load_string(KV)
    
class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class DummyScreen(Screen):
    pass

class StatusScreen(Screen):
    def on_enter(self):
        print('checking SSH')
        self.check_ssh()

    def check_ssh(self):
        try:
            # ssh = paramiko.SSHClient()
            # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh.connect(hostname = ssh_hostname, username = ssh_username, password = ssh_password, timeout=1)
            print('========================================= Connected SSH! (Dummy)')
            # to remove
            # self.ids.sshtest.text =  "SSH: Connected"
            # command = 'python location.py'
            # (stdin, stdout, stderr) = ssh.exec_command(command)
            # for line in stdout.readlines():
            #     # values=line[1:len(line)-3].split(",")
            #     print(line)
            #     print(type(line))
            self.ids.progress_percent0.current_percent = 85
            self.ids.progress_percent1.current_percent = 25
            self.ids.progress_percent2.current_percent = 35
        except socket.error as socket_err:
            self.ids.sshtest.text =  "SSH: Not Connected"
            print(socket_err)
        except paramiko.AuthenticationException as auth_err:
            print('========================================= Not Connected SSH!')
            print(auth_err)

    def power_on(self):
        try:
            # ssh = paramiko.SSHClient()
            # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh.connect(hostname = ssh_hostname, username = ssh_username, password = ssh_password, timeout=1)
            print('========================================= Connected SSH! (Dummy)')
            # command = 'cd Notebooks/OWR/REMOTE_ACCESS; ls; jupyter nbconvert --to notebook --execute Left.ipynb; jupyter nbconvert --to notebook --execute Right.ipynb'
            # (stdin, stdout, stderr) = ssh.exec_command(command)
            # for line in stdout.readlines():
            #     print(line)
            print('powered on')
            self.ids['power_on'].disabled = False
            self.ids['power_on'].opacity = 1
            self.ids['power_on'].pos = (275, 150)
            self.ids['power_off'].disabled = True
            self.ids['power_off'].opacity = 0
            self.ids['power_off'].pos = (0, 0)
            
        except socket.error as socket_err:
            print(socket_err)
        except paramiko.AuthenticationException as auth_err:
            print('========================================= Not Connected SSH!')
            print(auth_err)

    def power_off(self):
        try:
            # ssh = paramiko.SSHClient()
            # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh.connect(hostname = ssh_hostname, username = ssh_username, password = ssh_password, timeout=1)
            print('========================================= Connected SSH!')
            # command = 'cd Notebooks/OWR/REMOTE_ACCESS; ls; jupyter nbconvert --to notebook --execute Left.ipynb; jupyter nbconvert --to notebook --execute Right.ipynb'
            # (stdin, stdout, stderr) = ssh.exec_command(command)
            # for line in stdout.readlines():
            #     print(line)
            print('powered off')
            self.ids['power_on'].disabled = True
            self.ids['power_on'].opacity = 0
            self.ids['power_on'].pos = (0,0)
            self.ids['power_off'].disabled = False
            self.ids['power_off'].opacity = 1
            self.ids['power_off'].pos = (275, 150)
        except socket.error as socket_err:
            print(socket_err)
        except paramiko.AuthenticationException as auth_err:
            print('========================================= Not Connected SSH!')
            print(auth_err)

class LocationScreen(Screen):
    def on_enter(self):
        # self.build_map()
        print('checking SSH for Location')
        # self.check_ssh()
        self.build_map()
        
    def build_map(self):
        mapview = MapView(zoom=11, lat=45.5017, lon=-73.5673)
        m1 = MapMarker(lat=45.5017, lon=-73.5673, source='icons/marker.png') 
        # mapview = MapView(zoom=11, lat=scopexx, lon=scopeyy)
        # m1 = MapMarker(lat=scopexx, lon=scopeyy, source='mapmarker.png') 
        mapview.add_marker(m1)
        self.add_widget(mapview)

    def check_ssh(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print('sshusername', ssh_username)
            ssh.connect(hostname = ssh_hostname, username = ssh_username, password = ssh_password, timeout=1)
            print('========================================= Connected SSH!')
            command = 'python location.py'
            (stdin, stdout, stderr) = ssh.exec_command(command)
            for line in stdout.readlines():
                values=line[1:len(line)-3].split(",")
                print(values)
                # print(type(line))
                scopexx = values[0]
                scopeyy = values[1]
                self.build_map()
        except socket.error as socket_err:
            print(socket_err)
        except paramiko.AuthenticationException as auth_err:
            print('========================================= Not Connected SSH!')
            print(auth_err)

class AlertsScreen(Screen):
    def on_enter(self):
        print('=========================================entered alerts!')
        self.check_connection()

    def check_connection(self):
        try:
            # Check all urls and make sure they're up
            requests.get("https://teststorageaccount133.blob.core.windows.net/owr/data/alerts.json")
            print('Alerts: Connected')
            self.load_table()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err} - END')
            self.add_missing_sql()
        except Exception as err:
            print(f'Other error occurred: {err} - END')
            self.add_missing_sql()

    def load_table(self):
        data = requests.get("https://teststorageaccount133.blob.core.windows.net/owr/data/alerts.json")
        data.raise_for_status()
        row_data = data.json()
        print("====run_data data ", row_data[0])
        print("====run_data data ", row_data[0][1])
        layout = BoxLayout()
        self.data_tables = MDDataTable(
            # was .475 4/4/1am
            pos_hint={'center_y': 0.48, 'center_x': 0.5},
            size_hint=(0.4, 0.93),
            rows_num=len(row_data),
            # background_color= '#009dff',
            column_data=[
                ("Alert", dp(25)),
                ("Note", dp(25)),
                ("Time Stamp", dp(25))
                ],
            row_data=[(f"{row_data[0][0]}", f"{row_data[0][1]}", f"{row_data[i][2]}") for i in range(len(row_data))])
            #row_data=[(row[0][0], row[0][1], row[0][2], row[1][0], row[1][1], row[1][2])]
            #)
        layout.add_widget(self.data_tables)
        self.add_widget(layout)

#             pos_hint={'center_y': 0.44, 'center_x': 0.5},
#             size_hint=(0.4, 0.9),
#             rows_num=len(row),
#             # background_color= '#009dff',
#             column_data=[
#                 ("[font=fonts\Arialn.ttf][b]Alert[/b][/font]", dp(20)),
#                 ("[font=fonts\Arialn.ttf]Note[/font]", dp(20)),
#                 ("[font=fonts\Arialn.ttf]Time Stamp[/font]", dp(20))
#                 ],
#             row_data=[(f"{row[0][0]}", f"{row[0][1]}", f"{row[i][2]}") for i in range(len(row))])
#             #row_data=[(row[0][0], row[0][1], row[0][2], row[1][0], row[1][1], row[1][2])]
#             #)
#         screen.add_widget(data_tables)
#         self.add_widget(screen)

    def add_missing_sql(self):
        print('=========================================3.Add sql not Connected!')
        self.ids["sql_label"].text = "SQL Database Connection Failed!"
        self.ids["sql_retry_button"].disabled = False
        self.ids["sql_retry_button"].opacity = 1

class ControlsScreen(Screen):
    def switch1(self, checkbox, value):
        id = self.ids.sw_1
        if value: 
            print('Switch: sw_1:{}: On'.format(id))
        else:
            print('Switch: sw_1:{}: Off'.format(id))

    def switch2(self, checkbox, value):
        id = self.ids.sw_2
        if value: 
            print('Switch: sw_2:{}: On'.format(id))
        else:
            print('Switch: sw_2:{}: Off'.format(id))
    
    def switch3(self, checkbox, value):
        id = self.ids.sw_3
        if value: 
            print('Switch: sw_3:{}: On'.format(id))
        else:
            print('Switch: sw_3:{}: Off'.format(id))

    def switch4(self, checkbox, value):
        id = self.ids.sw_4
        if value: 
            print('Switch: sw_4:{}: On'.format(id))
        else:
            print('Switch: sw_4:{}: Off'.format(id))

class ScopeScreen(Screen):
    def on_enter(self):
        print('checking SSH for Scope')
        self.check_ssh()

    def check_ssh(self):
        try:
            # ssh = paramiko.SSHClient()
            # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh.connect(hostname = ssh_hostname, username = ssh_username, password = ssh_password, timeout=1)
            # print('========================================= Connected SSH!')
            # command = 'python location.py'
            # (stdin, stdout, stderr) = ssh.exec_command(command)
            # for line in stdout.readlines():
            #     # values=line[1:len(line)-3].split(",")
            #     print(line)
            #     print(type(line))
            
            scopexx =  45.50844171386265
            scopeyy = -73.58991198268038

        except socket.error as socket_err:
            scopexx =  45.50844171386265
            scopeyy = -73.58991198268038
            print('failed', scopexx)
            print('failed', scopeyy)
            print(socket_err)
        except paramiko.AuthenticationException as auth_err:
            print('========================================= Not Connected SSH!')
            print(auth_err)


class MapViewClass(MapView):
    def add_marker1(self):
        self.ids.marker_1.lat = self.lat
        self.ids.marker_1.lon = self.lon
        print('Marker1 coordinates - x: {}, y: {}'.format(self.lat, self.lon))
        self.ids['assign_marker_1'].disabled = True
        self.ids['assign_marker_1'].opacity = 0
        self.ids['assign_marker_1'].pos = (0, 60)
        self.ids['assign_marker_2'].disabled = False
        self.ids['assign_marker_2'].opacity = 1
        self.ids['assign_marker_2'].pos = (0, 0)
        
    def add_marker2(self):
        self.ids.marker_2.lat = self.lat
        self.ids.marker_2.lon = self.lon
        print('Marker2 coordinates - x: {}, y: {}'.format(self.lat, self.lon))
        self.ids['assign_marker_2'].disabled = True
        self.ids['assign_marker_2'].opacity = 0
        self.ids['assign_marker_2'].pos = (0, 60)
        self.ids['assign_marker_3'].disabled = False
        self.ids['assign_marker_3'].opacity = 1
        self.ids['assign_marker_3'].pos = (0, 0)
        # test math for coordinates
        abslat = self.ids.marker_1.lat - self.ids.marker_2.lat
        abslon = self.ids.marker_1.lon - self.ids.marker_2.lon
        print('abslat', abslat)
        print('abslon', abslon)
        # for i in range(10):
        #     marker = MapMarker(lat = self.ids.marker_1.lat, lon = self.ids.marker_1.lon)
        #     self.ids.mapview.add_widget(marker)
        marker = MapMarker(lat = self.ids.marker_1.lat + 0.01, lon = self.ids.marker_1.lon)
        self.add_widget(marker)
        # print("mapview", self.ids)

    def add_marker3(self):
        self.ids.marker_3.lat = self.lat
        self.ids.marker_3.lon = self.lon
        print('Marker3 coordinates - x: {}, y: {}'.format(self.lat, self.lon))  
        self.ids['assign_marker_3'].disabled = True
        self.ids['assign_marker_3'].opacity = 0
        self.ids['assign_marker_3'].pos = (0, 60)
        self.ids['assign_marker_4'].disabled = False
        self.ids['assign_marker_4'].opacity = 1
        self.ids['assign_marker_4'].pos = (0, 0)

    def add_marker4(self):
        self.ids.marker_4.lat = self.lat
        self.ids.marker_4.lon = self.lon
        print('Marker4 coordinates - x: {}, y: {}'.format(self.lat, self.lon))
        self.ids['assign_marker_4'].disabled = True
        self.ids['assign_marker_4'].opacity = 0
        self.ids['assign_marker_4'].pos = (0, 60)
        self.ids['remove_markers'].disabled = False
        self.ids['remove_markers'].opacity = 1
        self.ids['remove_markers'].pos = (0, 0)

    def remove_markers(self):
        self.ids.marker_1.lat = 0
        self.ids.marker_1.lon = 0
        self.ids.marker_2.lat = 0
        self.ids.marker_2.lon = 0
        self.ids.marker_3.lat = 0
        self.ids.marker_3.lon = 0
        self.ids.marker_4.lat = 0
        self.ids.marker_4.lon = 0
        self.ids['remove_markers'].disabled = True
        self.ids['remove_markers'].opacity = 0
        self.ids['remove_markers'].pos = (0, 60)
        self.ids['assign_marker_1'].disabled = False
        self.ids['assign_marker_1'].opacity = 1
        self.ids['assign_marker_1'].pos = (0, 0)


class RemoteAccessScreen(Screen):
    def on_enter(self):
        print('========================================= Remote Access')
        self.check_ssh()
   
    def check_ssh(self):
        try:
            ssh = paramiko.SSHClient()
            print('========================================= Connecting 1')
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print('========================================= Connecting 2')
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname = ssh_hostname, username = ssh_username, password = ssh_password, timeout=1)
            print('========================================= Connected SSH!')
        except socket.error as socket_err:
            print('========================================= Not Connected SSH!')
            print(socket_err)
        except paramiko.AuthenticationException as auth_err:
            print('========================================= Not Connected SSH!')
            print(auth_err)


    def turn_left(self):
        if(self.check_ssh()):
            print('turning left')
            command = 'cd Notebooks/OWR/Remote_Access; ls; jupyter nbconvert --to notebook --execute Left.ipynb;'
            # command = 'cd Notebooks/OWR/Remote_Access; ls; jupyter --execute Left.nbconvert.ipynb;'
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname = ssh_hostname, username = ssh_username, password = ssh_password, timeout=1)
            # command = 'cd Notebooks/OWR/Remote_Access; ls'
            (stdin, stdout, stderr) = ssh.exec_command(command)
            for line in stdout.readlines():
                print(line)
        else:
            self.ids.left.disabled = True
        
    def turn_right(self):
        if(self.check_ssh()):
            print('turning right')
            command = 'cd Notebooks/OWR/Remote_Access; ls; jupyter nbconvert --to notebook --execute Right.ipynb;'
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname = ssh_hostname, username = ssh_username, password = ssh_password, timeout=1)
            # command = 'cd Notebooks/OWR/Remote_Access; ls'
            (stdin, stdout, stderr) = ssh.exec_command(command)
            for line in stdout.readlines():
                print(line)
            command = 'cd Notebooks/OWR/REMOTE_ACCESS; ls; jupyter nbconvert --to notebook --execute Left.ipynb; jupyter nbconvert --to notebook --execute Right.ipynb'
            command = 'cd Notebooks/OWR/REMOTE_ACCESS; ls; jupyter nbconvert --execute Right.ipynb'
            (stdin, stdout, stderr) = self.ssh.exec_command(command)
            for line in stdout.readlines():
                print(line)
    

    def forward(self):
        if(self.check_ssh()):
            print('turning forward')
            command = 'cd Notebooks/OWR/REMOTE_ACCESS; ls; jupyter nbconvert --execute Forward.ipynb'
            (stdin, stdout, stderr) = self.ssh.exec_command(command)
            for line in stdout.readlines():
                print(line)

    def backward(self):
        if(self.check_ssh()):
            print('turning backward')
            command = 'cd Notebooks/OWR/REMOTE_ACCESS; ls; jupyter nbconvert --execute Backward.ipynb'
            (stdin, stdout, stderr) = self.ssh.exec_command(command)
            for line in stdout.readlines():
                print(line)

global file_iterator
file_iterator = 1
class DatabaseScreen(Screen):
    def on_enter(self):
        print('=========================================entered databseScreen!')
        self.check_connection()
    
    def check_connection(self):
        try:
            requests.get("https://teststorageaccount133.blob.core.windows.net/owr/data/owrData.txt")
            print('=========================================check_connection- True')
            # self.download(file_iterator)
            self.grid()

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err} - END')
            self.add_missing_sql()
        except Exception as err:
            print(f'Other error occurred: {err} - END')
            self.add_missing_sql()
    
    # def download(self, file_iterator):
    #     if(file_iterator == 10):
            
    #         return self.grid(file_iterator)
    #     print('=========================================check_connection- True')
    #     try:  
    #         print('test1', file_iterator)
    #         url_base = "https://teststorageaccount133.blob.core.windows.net/owr/database/"
    #         url_tip = "img{}.jpg".format(file_iterator)
    #         print(url_base+url_tip)
    #         r = requests.get(url_base+url_tip)
    #         with open("database/img{}.jpg".format(file_iterator), 'wb') as f:
    #             for chunk in r:
    #                 f.write(chunk)
    #         file_iterator = file_iterator + 1
    #         print(file_iterator)
    #         print('true')
    #         self.download(file_iterator)
    #     except:
    #         print('error')
    #     print('done downloading')
    #     self.grid(file_iterator)

    # def grid(self, file_iterator):
    #     # Images 
    #     print('file', file_iterator)
    #     j = 1
    #     while j < file_iterator:
    #         data = "database/img{}.jpg".format(j)
    #         print('data', data)
    #         image = Image(source=data, allow_stretch= True, keep_ratio = False)
    #         self.ids.container.add_widget(image)
    #         j = j+1
    #     self.ids.sql_label.text = ""

        # image = Image(source="database/img1.jpg")
        # self.ids.container.add_widget(image)
      
    def grid(self):
        # Images 
        # j = 1
        # while j < 8:
        #     data = "database/img{}.jpg".format(j)
        #     print('data', data)
        #     image = Image(source=data, allow_stretch= False, keep_ratio = False)
        #     self.ids.container.add_widget(image)
        #     j = j+1
        data = "database/img1.jpg"
        image = Image(source=data, allow_stretch= False, keep_ratio = False)
        self.ids.container.add_widget(image)

        data = "database/img2.jpg"
        image = Image(source=data, allow_stretch= False, keep_ratio = False)
        self.ids.container.add_widget(image)

        data = "database/img3.jpg"
        image = Image(source=data, allow_stretch= False, keep_ratio = False)
        self.ids.container.add_widget(image)

        data = "database/img4.jpg"
        image = Image(source=data, allow_stretch= False, keep_ratio = False)
        self.ids.container.add_widget(image)

        data = "database/img5.jpg"
        image = Image(source=data, allow_stretch= False, keep_ratio = False)
        self.ids.container.add_widget(image)

        data = "database/img6.jpg"
        image = Image(source=data, allow_stretch= False, keep_ratio = False)
        self.ids.container.add_widget(image)
    
        self.ids.sql_label.text = ""
    

    def add_missing_sql(self):
        print('=========================================3.Add sql not Connected!')
        self.ids["sql_label"].text = "SQL Database Connection Failed!"
        self.ids["sql_retry_button"].disabled = False
        self.ids["sql_retry_button"].opacity = 1
class StatisticsScreen(Screen):
    pass
    def on_enter(self):
        print("====entered")
        print('id value', self.name)
        self.check_connection()
   
    def check_connection(self):
        try:
            # Check all urls and make sure they're up
            requests.get("https://teststorageaccount133.blob.core.windows.net/owr/data/material_stats.json")
            print('Material_stats: Connected')
            requests.get("https://teststorageaccount133.blob.core.windows.net/owr/data/bar_stats.json")
            print('Bar_stats: Connected')
            requests.get("https://teststorageaccount133.blob.core.windows.net/owr/data/run_stats.json")
            print('Run_stats: Connected')
            
            self.create_chart()
            self.set_bar_data()
            self.create_table()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err} - END')
            self.add_missing_sql()
        except Exception as err:
            print(f'Other error occurred: {err} - END')
            self.add_missing_sql()

    def add_missing_sql(self):
        print('=========================================3.Add sql not Connected!')
        self.ids["sql_label"].text = "SQL Database Connection Failed!"
        self.ids["sql_retry_button"].disabled = False
        self.ids["sql_retry_button"].opacity = 1
        self.ids["sql_retry_button"].background_normal = ""
        self.ids["sql_retry_button"].background_color = (1, 1, 1, 1)

     # Pie chart methods
    def create_chart(self):
        data = requests.get("https://teststorageaccount133.blob.core.windows.net/owr/data/material_stats.json")
        data.raise_for_status()
        chart_data = data.json()
        # print("====chart data ", chart_data[0])
        # print("====chart data ", chart_data[0][1])
        collection = [" ", chart_data[0][0]]
        positive_id = ["  ", chart_data[0][1]]
        negative = ["   ", chart_data[0][2]]
        wrong = ["    ", chart_data[0][3]]
        missed = ["     ", chart_data[0][4]]

        metal_collection = [" ", chart_data[0][5]]
        metal_positive_id = ["  ", chart_data[0][6]]
        metal_negative = ["   ", chart_data[0][7]]
        metal_wrong = ["    ", chart_data[0][8]]
        metal_missed = ["     ", chart_data[0][9]]
        # create 2 pies
        self.piechart = AKPieChart(
            size_hint=[None, None],
            size=(dp(150), dp(150)),
            pos_hint= {"x": 0.01, 'y': 0.65},
            # on_leave= root.remove_chart()
            items = [{collection[0]: collection[1], positive_id[0]: positive_id[1], negative[0]: negative[1], wrong[0]: wrong[1], missed[0]: missed[1]}]
        )
        self.piechart2 = AKPieChart(
            size_hint=[None, None],
            size=(dp(150), dp(150)),
            pos_hint= {"x": 0.02, 'y': 0.65},
            items = [{metal_collection[0]: metal_collection[1], metal_positive_id[0]: metal_positive_id[1], metal_negative[0]: metal_negative[1], metal_wrong[0]: metal_wrong[1], metal_missed[0]: metal_missed[1]}]
        )
        self.ids.chart_box.add_widget(self.piechart)
        self.ids.chart_box2.add_widget(self.piechart2)
        
        # self.remove_chart()
    
    # Bar method
    def set_bar_data(self):
        try:
            data = requests.get("https://teststorageaccount133.blob.core.windows.net/owr/data/bar_stats.json")
            data.raise_for_status()
            jsonResponse = data.json()

            barchart = AKBarChart(size_hint_y = 0.2,
            size_hint_x = 0.9,
            x_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            y_values = [(jsonResponse[0][i]) for i in range(len(jsonResponse[0]))],
            label_size = dp(10),
            pos_hint= {"x": 0.05, 'y': 0.65},
            labels= True, anim= True,
            lines_color= [0.6, 0, 0.4, 1],
            bars_color= [0, 0, 0.4, 1])
            self.add_widget(barchart)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err} - END')
            self.add_missing_sql()
        except Exception as err:
            print(f'Other error occurred: {err} - END')
            self.add_missing_sql()


    def create_table(self):
        try:
            data = requests.get("https://teststorageaccount133.blob.core.windows.net/owr/data/run_stats.json")
            data.raise_for_status()
            run_data = data.json()
            print("====run_data data ", run_data[0])
            print("====run_data data ", run_data[0][1])
            layout = BoxLayout()
            self.data_tables = MDDataTable(
                pos_hint={'center_y': 0.14, 'center_x': 0.5},
                size_hint=(0.4, 0.3),
                rows_num=3,
                # background_color= '#009dff',
                column_data=[
                    ("Run", dp(21)),
                    ("Recovery", dp(25)),
                    ("RunTime", dp(25))
                ],
                row_data=[
                    (run_data[0][0],run_data[0][1],run_data[0][2]),
                    ("","","")])
            layout.add_widget(self.data_tables)
            self.add_widget(layout)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err} - END')
            self.add_missing_sql()
        except Exception as err:
            print(f'Other error occurred: {err} - END')
            self.add_missing_sql()

    def on_leave(self):
        self.ids.chart_box.remove_widget(self.piechart)
        self.ids.chart_box2.remove_widget(self.piechart2)

    
if __name__ == '__main__':
    app = MainApp()
    app.run()
