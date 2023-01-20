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
import os, sys
from kivy.resources import resource_add_path, resource_find

Builder.load_file('emotion_detection/kv_file.kv')
model = process_image.Model("emotion_detection/model.json", "emotion_detection/model_weights.h5")

class MenuScreen(Screen):
    pass

class CameraScreen(Screen):
    def detect_mood(self):
        camera = self.ids.camera
        timestr = time.strftime("%Y%m%d_%H%M%S")
        path = "emotion_detection/user_images/IMG_{}.png".format(timestr)

        camera.export_to_png(path)

        img = model.load_img_from_path(path)
        mood = model.predict_emotion(img)

        self.ids.mood_label.text = "Mood Detected: " + mood
        file = open("emotion_detection/moodlog.txt", "a") 
        file.write("{}\n".format(mood))
        file.close()
        return 0
    def on_enter(self):
        self.ids.mood_label.text = "Mood Detected: "

class GalleryScreen(Screen):
    def on_enter(self):
        for i in range(1, 10):
            self.ids['image{}'.format(i)].source = 'emotion_detection/blank.png'
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
        self.manager.current = 'home'

class SignupScreen(Screen):
    def process(self):
        username = self.ids.input_user.text
        password = self.ids.input_pass.text
        self.manager.current = 'home'

class HomeScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass

class LogScreen(Screen):
    def pie_chart(self):
        labels = []
        sizes = []
        dict_labels = {'Angry': 0, 'Disgust': 0, 'Fear': 0, 'Happy': 0, 'Sad': 0, 'Surprised': 0, 'Neutral': 0}
        timestr = time.strftime("%Y%m%d_%H%M%S")

        file = open("emotion_detection/moodlog.txt", "r") 
        for line in file.readlines():
            dict_labels[line.strip()] += 1
        file.close()

        for emote in dict_labels:
            if dict_labels[emote] > 0:
                labels.append(emote)
                sizes.append(dict_labels[emote])
        
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal') 
        plt.savefig('emotion_detection/user_plots/pie_chart_{}.png'.format(timestr))
        self.ids.image.source = 'emotion_detection/user_plots/pie_chart_{}.png'.format(timestr)

    def on_enter(self):
        self.ids.image.source = 'emotion_detection/blank.png'

class MainApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        LabelBase.register(name='Lucida',
                      fn_regular='emotion_detection/lucida/Lucida.ttf')   
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