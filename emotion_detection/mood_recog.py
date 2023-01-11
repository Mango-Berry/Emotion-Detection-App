from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
import time

Builder.load_string('''
<CameraScreen>:
    BoxLayout:
        orientation: 'vertical'
        Camera:
            id: camera
            play: True
        Button:
            text: 'Capture'
            on_press: root.capture()
            background_normal: 'button.png'

<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            color: 0, 0, 0, 1
            text: 'Emotion Detection'
            size_hint: 0.4, 0.3
            pos_hint: {'center_x':.5, 'center_y':.25}
        Label:
            color: 0, 0, 0, 1
            text: 'Detect emotions and facial expressions in real-time with machine learning'
            size_hint: 0.4, 0.3
            pos_hint: {'center_x':.5, 'center_y':.5}
        Button:
            text: 'Login'
            background_normal: 'button.png'
            on_press: root.manager.current = 'login'
            size_hint: 0.4, 0.2
            pos_hint: {'center_x':.5, 'center_y':.7}
        Button:
            text: 'Signup'
            background_normal: 'button.png'
            on_press: root.manager.current = 'signup'
            pos_hint: {'center_x':.5, 'center_y': .8}
            size_hint: 0.4, 0.2
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: input_user
            hint_text:'Enter username'
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
            multiline:False
        TextInput:
            id: input_pass
            hint_text:'Enter password'
            pos_hint: {'center_x': 0.5, 'center_y': 0.2}
            multiline:False
        Button:
            text: 'Enter'
            background_normal: 'button.png'
            on_press: root.manager.current = 'home'
            size_hint: 0.4, 0.2
            pos_hint: {'center_x':.5, 'center_y':.7}
<SignupScreen>:
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: input_user
            hint_text:'Enter username'
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
            multiline:False
        TextInput:
            id: input_pass
            hint_text:'Enter password'
            pos_hint: {'center_x': 0.5, 'center_y': 0.2}
            multiline:False
        Button:
            text: 'Enter'
            background_normal: 'button.png'
            on_press: root.process()
            size_hint: 0.4, 0.2
            pos_hint: {'center_x':.5, 'center_y':.7}
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            color: 0, 0, 0, 1
            text: 'Detect emotions and facial expressions in real-time with machine learning'
            size_hint: 0.4, 0.3
            pos_hint: {'center_x':.5, 'center_y':.3}
        Button:
            text: 'Camera'
            background_normal: 'button.png'
            on_press: root.manager.current = 'camera'
            size_hint: 0.4, 0.2
            pos_hint: {'center_x':.5, 'center_y':.7}
        Button:
            text: 'Gallery'
            background_normal: 'button.png'
            on_press: root.manager.current = 'gallery'
            pos_hint: {'center_x':.5, 'center_y': .8}
            size_hint: 0.4, 0.2
        Button:
            text: 'Profile'
            background_normal: 'button.png'
            on_press: root.manager.current = 'camera'
            size_hint: 0.4, 0.2
            pos_hint: {'center_x':.5, 'center_y':.9}
        Button:
            text: 'Stats'
            background_normal: 'button.png'
            on_press: root.manager.current = 'gallery'
            pos_hint: {'center_x':.5, 'center_y': 1}
            size_hint: 0.4, 0.2
''')


class CameraScreen(Screen):
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("user_images/IMG_" + timestr)
        print("captured")


class MenuScreen(Screen):
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
        sm.add_widget(CameraScreen(name='camera'))
        return sm


if __name__ == '__main__':
    MainApp().run()
