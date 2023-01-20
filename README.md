# Moodsense: An Emotion Detection App
- A colaborative app produced using python. This app looks at images and, using a convolutional neural network, tells the user its best guess of what the emotion showcased in the image may be.

# The App
- There are 6 main screens in the app: the welcome page, login, signup, home screen, camera, gallery, and mood log
- All are completely functional except for the login and signup which are missing their authentication backend at this time
- The app can access your device's camera to take a picture, guess the emotion in the image, save the image on local storage, and create a pie chart of your emotions.

# How it works:
- The neural network found in the file GroupProjectCNN was trained on a database of over 22000 images.
- Then, the model was exported to json (model.json file) with the weights being saved to model_weights.h5
- In order to run, there is the primary file main.py, as well as supporting files for images and textures, as well as the model files mentioned above.
- These rely on libraries like os, TensorFlow, Pandas, Kivy, and other which can be found at the top of the above files. 
- When main.py is ran, the app pops up and works like the demo above. 

# Goals
- To learn more about neural networks
- To create something that people can use, specifically for those who have difficulty identifying emotions

# Accomplished
- The app was created almost to completion before problems were run into, primarily due to the projects due date, limiting the time we can work to 3 weeks.
- Any of us may come back to the project in the future, so look out on all of the contributor's GitHub pages :)