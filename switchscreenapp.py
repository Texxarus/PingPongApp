from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
)
class LoginPage(Screen):

    text_label = StringProperty("Enter your name here!")

    def verify_credentials(self):
        if self.ids["login"].text == "Quốc":
            self.manager.current = "user"
        else:
            self.text_label = "Wrong! Your name is Quốc. Enter \"Quốc\" now!"

class UserPage(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass



#kv_file = Builder.load_file('login.kv')

class SwitchScreenApp(App):
    def builder(self):
        return ScreenManagement

if __name__ == '__main__':
    SwitchScreenApp().run()
