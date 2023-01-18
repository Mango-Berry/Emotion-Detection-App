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
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import sqlite3
from threading import Thread

Builder.load_file('emotion_detection/kv_file.kv')

class MenuScreen(Screen):
    pass

class CameraScreen(Screen):
    def detect_mood(self):
        camera = self.ids.camera
        timestr = time.strftime("%Y%m%d_%H%M%S")

        #insert cnn code here (specifcally the mood detecting function call)
        mood = 'Happy'
        dict_labels = {'Angry': 1, 'Disgust': 2, 'Fear': 3, 'Happy': 4, 'Sad': 5, 'Surprised': 6, 'Neutral': 7}
        camera.export_to_png("emotion_detection/user_images/IMG_{}_{}.png".format(timestr, dict_labels[mood]))
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
        input_username = self.ids.input_user.text
        input_password = self.ids.input_pass.text
        if main_app.login(input_username, input_password):
            ScreenManager.switch_to = 'home'

class SignupScreen(Screen):
    def process(self):
        input_username = self.ids.input_user.text
        input_password = self.ids.input_pass.text
        if main_app.register(input_username, input_password):
            ScreenManager.switch_to = 'home'
        
class HomeScreen(Screen):
    @login_required
    def logout(self):
        logout_user()
        ScreenManager.switch_to = 'menu'

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
        sm.add_widget(LogScreen(name='log'))
        Thread(target=self.start_flask).start()
        return sm

    def start_flask(self):
        self.flask_app = Flask(__name__)
        self.db = SQLAlchemy(self.flask_app)
        self.bcrypt = Bcrypt(self.flask_app)

        self.flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
        self.flask_app.config["SECRET_KEY"] = "Secret Key"
        self.db.init_app(self.flask_app)

        login_manager = LoginManager()
        login_manager.init_app(self.flask_app)
        login_manager.login_view = "login"

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        class User(self.db.Model, UserMixin):
            id = self.db.Column(self.db.INTEGER, primary_key=True)
            username = self.db.Column(self.db.String(20), nullable=False, unique=True)
            password = self.db.Column(self.db.String(80), nullable=False)
        self.User = User()
        self.flask_app.run(debug=True)

    def login(self, input_username, input_password):
        with self.flask_app.app_context():
            user = self.User.query.filter_by(username=input_username).first()    
            if user:
                if self.bcrypt.check_password_hash(user.password, input_password):
                    login_user(user)

    def register(self, input_username, input_password):
        with self.flask_app.app_context():
            hashed_password = self.bcrypt.generate_password_hash(input_password)
            new_user = self.User(username=input_username, password=hashed_password)
            self.db.session.add(new_user)
            self.db.session.commit()

main_app = MainApp()
main_app.run()
