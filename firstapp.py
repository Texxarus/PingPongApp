from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, ListProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
import time
from kivy.core.window import Window
#Window.size = (1500, 600)
v_x_init = Window.width / 50 # = 20 for width 1000, = 30 for width 1500

class PongPaddle(Widget):
    score = NumericProperty(0)
    time_bounce = time.time()

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            #print ("Rounded Time: ", round(time.time() - self.time_bounce))
            if self.collide_widget(ball):
                vx, vy = ball.velocity
                offset = (ball.center_y - self.center_y) / (self.height / 2)
                bounced = Vector(-1 * vx, vy)

                #vel = bounced * 1.1
                #ball.velocity = vel.x, vel.y + offset
                        
                vel = bounced[0], bounced[1] * 1.1
                ball.velocity = round(vel[0], 1), round(vel[1], 1) + offset*1.5
            self.time_bounce = time.time()

            #ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    p1_score = NumericProperty(0)
    p2_score = NumericProperty(0)
    motion = NumericProperty(0)
    last_won = NumericProperty(1)

    
    def serve_ball(self, vel=(v_x_init, 1)):
        #print("inside serveball")
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()
        #self.motion = 10
        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        #print(self.width, v_x_init)
        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        self.p1_score = self.player1.score
        self.p2_score = self.player2.score
        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(v_x_init, 1))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-v_x_init, -1))
        if(self.parent.manager.option == 1):
            self.motion = 10
            if self.ball.velocity_x < 0:
                if(abs(self.player1.center_y - self.ball.center_y) > 10):
                    if (self.player1.center_y < self.ball.center_y):
                        self.player1.center_y += self.motion
                        #self.motion += 2
                        if self.player1.center_y > self.height: # checking if paddle goes above max height
                            self.player1.center_y = self.height
                    else:
                        self.player1.center_y -= self.motion
                        #self.motion += 2
                        if self.player1.center_y < 0: # if paddle goes below zero
                            self.player1.center_y = 0
        

    def on_p1_score(self, instance, value):
        #print('My p1score changed to', value)
        self.last_won = 1

        if (value <= 5 and value > 0):
            self.parent.pausing()
            self.parent.manager.value = value - 1
            Clock.schedule_once (self.switch_to_KatsWin, 0.5)

        if value == 5:
            self.player2.score = 0
            self.player1.score = 0

    def on_p2_score(self, instance, value):
        #print('My p2score changed to', value)   
        self.last_won = -1
        
        if (value <=5 and value > 0):
            self.parent.pausing()
            self.parent.manager.value = value - 1
            Clock.schedule_once (self.switch_to_QuocWin, 0.5)

        if value == 5:
            self.player2.score = 0
            self.player1.score = 0

    def switch_to_QuocWin(self, dt):
        self.parent.manager.current = "quocwin_page"

    def switch_to_KatsWin(self, dt):
        self.parent.manager.current = "katswin_page"

    def on_touch_move(self, touch):
        if (touch.x < self.width / 3) and (self.parent.manager.option == 2) :
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

class LoginPage(Screen):

    text_label = StringProperty("Enter your name here!")

    def verify_credentials(self):
        if self.ids["login"].text == "Quoc":
            self.manager.current = "option_page"
        else:
            self.text_label = "Wrong! Your name is Quoc. Enter \"Quoc\" now!"

class PlayingPage(Screen):
    
    enter_count = NumericProperty(0)
    event = ObjectProperty(None)
    def playing(self):
        self.enter_count += 1
        
        self.ids.my_pong_game.serve_ball(vel=(self.ids.my_pong_game.last_won*v_x_init, self.ids.my_pong_game.last_won*1))
        self.ids.my_pong_game.player2.center_y = self.ids.my_pong_game.center_y
        self.ids.my_pong_game.player1.center_y = self.ids.my_pong_game.center_y
        self.event = Clock.schedule_interval(self.ids.my_pong_game.update, 1.0 / 60.0)    

    def pausing(self):
        #print("Inside Pausing funtion")
        self.event.cancel()  

class OptionPage(Screen):
    
    def one_player(self):
        self.manager.option = 1
        self.manager.current = "playing_page"
    def two_player(self):
        self.manager.option = 2
        self.manager.current = "playing_page"


class QuocWin(Screen):
    
    #img_source = StringProperty(None)
    def on_touch_down(self, touch):
        if (self.manager.value == 4):
            self.manager.current = "option_page"
        else:
            self.manager.current = "playing_page"

class KatsWin(Screen):
    def on_touch_down(self, touch):
        if (self.manager.value == 4):
            self.manager.current = "option_page"
        else:
            self.manager.current = "playing_page"
    

class ScreenManagement(ScreenManager):
    option = NumericProperty(0)
    winner = StringProperty(None)
    value = NumericProperty(0)

    quoc_img = ListProperty(["quoc1.jpg", "quoc2.jpg", "quoc3.jpg", "quoc4.jpg", "quoc5.jpg"])
    kats_img = ListProperty(["kats1.jpg", "kats2.jpg", "kats3.jpg", "kats4.jpg", "kats5.jpg"])

class FirstApp(App):
    def builder(self):
        self.icon = 'app_icon.jpg'
        return ScreenManagement()

#class PongApp(App):
#    def build(self):
#        game = PongGame()
#        game.serve_ball()
#        Clock.schedule_interval(game.update, 1.0 / 60.0)
#        return game


if __name__ == '__main__':
    FirstApp().run()