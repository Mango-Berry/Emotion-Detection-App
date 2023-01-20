from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
import time, glob
import matplotlib.pyplot as plt
import Process_Image as process_image

Builder.load_file('emotion_detection/kv_file.kv')

class MenuScreen(Screen):
    pass

class CameraScreen(Screen):
    def detect_mood(self):
        camera = self.ids.camera
        timestr = time.strftime("%Y%m%d_%H%M%S")
        dict_labels = {'Angry': 1, 'Disgust': 2, 'Fear': 3, 'Happy': 4, 'Sad': 5, 'Surprised': 6, 'Neutral': 7}
        path = "emotion_detection/user_images/IMG_{}.png".format(timestr)

        camera.export_to_png(path)

        model = process_image.Model("model.json", "model_weights.h5")
        img = model.load_img_from_path(path)
        mood = model.predict_emotion(img)

        camera.export_to_png("emotion_detection/user_images_labeled/IMG_{}.png".format(dict_labels[mood]))
        self.ids.mood_label.text = "Mood Detected: " + mood
        file = open("moodlog.txt", "a") 
        file.write("{}\n".format(mood))
        file.close()
        return 0

class GalleryScreen(Screen):
    def __init__ (self, **kwargs):
        self.name='gallery'
        super().__init__(**kwargs)
        count = 1
        for file in sorted(glob.glob('emotion_detection/user_images/*.png')):
            if(count <= 9):
                self.ids['image{}'.format(count)].source = file
                count += 1
            else:
                break

class LoginScreen(Screen):
    def process(self):
        username = self.ids.input_user.text
        password = self.ids.input_pass.text
        # auth code
        ScreenManager.switch_to = 'home'

class SignupScreen(Screen):
    def process(self):
        username = self.ids.input_user.text
        password = self.ids.input_pass.text
        # auth code

class HomeScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass

class LogScreen(Screen):
    def pie_chart(self):
        labels = 'Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprised', 'Neutral'
        dict_labels = {'Angry': 0, 'Disgust': 0, 'Fear': 0, 'Happy': 0, 'Sad': 0, 'Surprised': 0, 'Neutral': 0}
        
        file = open("moodlog.txt", "r") 
        for line in file.readlines():
            dict_labels[line.strip()] += 1
        sizes = [dict_labels['Angry'], dict_labels['Disgust'], dict_labels['Fear'], dict_labels['Happy'], dict_labels['Sad'], dict_labels['Surprised'], dict_labels['Neutral'] ]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal') 
        plt.savefig('latest_plot.png')
        self.ids.image.source = 'latest_plot.png'

class MainApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        LabelBase.register(name='Lucida',
                      fn_regular='emotion_detection\lucida\Lucida.ttf')   
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CameraScreen(name='camera_page'))
        sm.add_widget(GalleryScreen(name='gallery'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(LogScreen(name='log'))
        return sm
MainApp().run()
