from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
import time
Builder.load_string('''
<CameraScreen>:
    orientation: 'vertical'
    Camera:
        id: camera
        play: True
    Button:
        text: 'Capture'
        height: '48dp'
        on_press: root.capture()

<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Goto settings'
            on_press: root.manager.current = 'settings'
        Button:
            text: 'Quit'

<HomeScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
''')

class CameraScreen(BoxLayout):
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_" + timestr)

class MenuScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class MainApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(HomeScreen(name='home'))
        return sm

if __name__ == '__main__':
    MainApp().run()

