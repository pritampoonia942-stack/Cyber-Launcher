import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
import time
import webbrowser
import random
import os

# --- सेटिंग्स ---
DEV_NAME = "PRITAM POONIA"
PASSWORD = "1234"

# कलर्स
NEO_GREEN = (0, 1, 0, 1)
NEO_RED = (1, 0, 0, 1)
NEO_DARK = (0.05, 0.05, 0.05, 1)
NEO_CYAN = (0, 1, 1, 1)
NEO_YELLOW = (1, 1, 0, 1)

Window.clearcolor = NEO_DARK

# --- स्क्रीन 1: लॉगिन ---
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.add_widget(Label(text="[ SYSTEM LOCKED ]", font_size='24sp', color=NEO_RED, bold=True))
        self.info = Label(text=f"USER: {DEV_NAME}", color=NEO_GREEN)
        self.layout.add_widget(self.info)
        self.pass_input = TextInput(multiline=False, password=True, background_color=(0.2,0.2,0.2,1), foreground_color=NEO_GREEN, cursor_color=NEO_GREEN, size_hint=(1, 0.2), halign='center', font_size='20sp')
        self.pass_input.bind(on_text_validate=self.check_pass)
        self.layout.add_widget(self.pass_input)
        self.btn = Button(text="UNLOCK", background_color=(0,0.5,0,1), size_hint=(1, 0.2))
        self.btn.bind(on_press=self.check_pass)
        self.layout.add_widget(self.btn)
        self.add_widget(self.layout)

    def check_pass(self, instance):
        if self.pass_input.text == PASSWORD:
            self.manager.current = 'launcher'
        else:
            self.info.text = "WRONG PASSWORD!"
            self.info.color = NEO_RED

# --- स्क्रीन 2: लॉन्चर ---
class LauncherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # टॉप बार
        info = BoxLayout(size_hint=(1, 0.08))
        self.date_lbl = Label(text="INIT...", color=NEO_GREEN, font_size='14sp', halign='left')
        self.batt_lbl = Label(text="SYS: ONLINE", color=NEO_GREEN, font_size='14sp', halign='right')
        info.add_widget(self.date_lbl); info.add_widget(self.batt_lbl)
        self.layout.add_widget(info)

        # घड़ी
        self.time_lbl = Label(text="00:00", font_size='70sp', color=(1,1,1,1), bold=True)
        self.layout.add_widget(self.time_lbl)

        # नाम
        self.layout.add_widget(Label(text=f"WELCOME, {DEV_NAME}", color=(0.5,0.5,0.5,1), font_size='13sp', size_hint=(1, 0.05), bold=True))

        # इनपुट
        self.layout.add_widget(Label(text="COMMAND CENTER >_", color=NEO_CYAN, size_hint=(1, 0.05)))
        self.search_input = TextInput(hint_text="Search / Hack / Read...", multiline=False, background_color=(0.2,0.2,0.2,1), foreground_color=NEO_GREEN, cursor_color=NEO_GREEN, size_hint=(1, 0.12), padding_y=[10, 0])
        self.search_input.bind(on_text_validate=self.process_command)
        self.layout.add_widget(self.search_input)

        # बटन ग्रिड
        grid = GridLayout(cols=4, spacing=5, size_hint=(1, 0.15))
        def mk_btn(n, c, cmd):
            b = Button(text=n, background_color=c, font_size='11sp')
            b.bind(on_press=lambda x: self.process_command(None, cmd=cmd))
            grid.add_widget(b)
        
        mk_btn("GAME", NEO_YELLOW, "game") # गेम बटन
        mk_btn("HACK", (0,0.5,0,1), "hack")
        mk_btn("READ", (0,0,1,1), "read")
        mk_btn("YT", (0.8,0,0,1), "youtube")
        self.layout.add_widget(grid)

        # लॉग
        self.log_lbl = Label(text="> SYSTEM READY...", color=NEO_GREEN, size_hint=(1, 0.25), text_size=(Window.width-20, None), halign='left', valign='top', font_size='11sp')
        self.layout.add_widget(self.log_lbl)
        
        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1)
        self.hacking_mode = False

    def update(self, dt):
        self.time_lbl.text = time.strftime("%H:%M")
        self.date_lbl.text = time.strftime("%d %b").upper()
        if self.hacking_mode:
            codes = ["01", "AF", "##", "run", "sys"]
            line = "".join([random.choice(codes)+" " for _ in range(8)])
            current = self.log_lbl.text.split('\n')
            if len(current)>8: current.pop(0)
            current.append(f"> {line}")
            self.log_lbl.text = "\n".join(current)

    def process_command(self, instance, cmd=None):
        q = cmd if cmd else self.search_input.text.strip()
        if not q: return
        c = q.lower()

        if c == "game": self.manager.current = 'game' # गेम स्क्रीन पर जाएं
        elif c == "hack": 
            self.hacking_mode = True
            self.log_lbl.text = "> HACKING STARTED..."
        elif c == "stop": 
            self.hacking_mode = False
            self.log_lbl.text = "> STOPPED."
        elif c.startswith("save:"):
            try: 
                with open("secret.txt","w") as f: f.write(q.split("save:")[1])
                self.log_lbl.text = "> SECRET SAVED."
            except: pass
        elif c == "read":
            if os.path.exists("secret.txt"):
                with open("secret.txt","r") as f: self.log_lbl.text = f"> SECRET: {f.read()}"
            else: self.log_lbl.text = "> NO DATA."
        elif c == "youtube": webbrowser.open("https://youtube.com")
        else: webbrowser.open(f"https://www.google.com/search?q={q}")
        if instance: self.search_input.text = ""

# --- स्क्रीन 3: गेम (Tic Tac Toe) ---
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # हेडर
        self.layout.add_widget(Label(text="TIC-TAC-TOE", font_size='30sp', color=NEO_YELLOW, size_hint=(1, 0.15), bold=True))
        self.turn_lbl = Label(text="TURN: X", color=NEO_GREEN, size_hint=(1, 0.1))
        self.layout.add_widget(self.turn_lbl)

        # गेम बोर्ड
        self.grid = GridLayout(cols=3, spacing=5)
        self.buttons = []
        for i in range(9):
            btn = Button(text="", font_size='40sp', background_color=(0.2,0.2,0.2,1))
            btn.bind(on_press=self.move)
            self.buttons.append(btn)
            self.grid.add_widget(btn)
        self.layout.add_widget(self.grid)

        # बैक बटन
        back = Button(text="< BACK TO SYSTEM", background_color=(1,0,0,1), size_hint=(1, 0.15))
        back.bind(on_press=self.go_back)
        self.layout.add_widget(back)
        
        self.add_widget(self.layout)
        self.turn = 'X'
        self.game_active = True

    def move(self, btn):
        if not self.game_active or btn.text != "": return
        btn.text = self.turn
        btn.color = NEO_GREEN if self.turn == 'X' else NEO_RED
        
        # जीत चेक करें
        if self.check_win():
            self.turn_lbl.text = f"WINNER: {self.turn}!"
            self.turn_lbl.color = NEO_YELLOW
            self.game_active = False
        elif all(b.text != "" for b in self.buttons):
            self.turn_lbl.text = "DRAW GAME!"
            self.game_active = False
        else:
            self.turn = 'O' if self.turn == 'X' else 'X'
            self.turn_lbl.text = f"TURN: {self.turn}"

    def check_win(self):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in wins:
            if self.buttons[a].text == self.buttons[b].text == self.buttons[c].text != "":
                return True
        return False

    def go_back(self, instance):
        # रिसेट करें और वापस जाएं
        for b in self.buttons: b.text = ""; b.color = (1,1,1,1)
        self.turn = 'X'; self.game_active = True; self.turn_lbl.text = "TURN: X"
        self.manager.current = 'launcher'

class NeoApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(LauncherScreen(name='launcher'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    NeoApp().run()
