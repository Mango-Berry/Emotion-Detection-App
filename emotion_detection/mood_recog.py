from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
import time

Builder.load_file('emotion_detection/kv_file.kv')

class MenuScreen(Screen):
    pass


class CameraScreen(Screen):
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("emotion_detection/user_images/IMG_{}.png".format(timestr))
    def recognize_mood(self):
        pass

class LoginScreen(Screen):
    def process(self):
        username = self.ids.input_user.text
        password = self.ids.input_pass.text
        # firebase
        ScreenManager.switch_to = 'home'


class SignupScreen(Screen):
    def process(self):
        username = self.ids.input_user.text
        password = self.ids.input_pass.text
        # firebase


class HomeScreen(Screen):
    pass

class MainApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CameraScreen(name='camera_page'))
        return sm
MainApp().run()
