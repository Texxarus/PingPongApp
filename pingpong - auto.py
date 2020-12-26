from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
import math
from kivy.vector import Vector
from kivy.clock import Clock
import time

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)

            #vel = bounced * 1.1
            #ball.velocity = vel.x, vel.y + offset
                       
            vel = bounced[0], bounced[1] * 1.1
            ball.velocity = round(vel[0], 1), round(vel[1], 1) + offset

            #print(vel, offset, bounced)
            #print(ball.velocity)

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        #self.pos = self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]
        print(self.pos[0], self.velocity_x)


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    motion = NumericProperty(10)
    def serve_ball(self, vel=(20, 1)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.motion = 5
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        if self.ball.velocity_x < 0:
            if(abs(self.player1.center_y - self.ball.center_y) > 10):
                if (self.player1.center_y < self.ball.center_y):
                    self.player1.center_y += self.motion
                    self.motion += 2
                    if self.player1.center_y > self.height: # checking if paddle goes above max height
                        self.player1.center_y = self.height
                    #kb.press_key('w')
                    #kb.release_key('w')
                else:
                    self.player1.center_y -= self.motion
                    self.motion += 2
                    if self.player1.center_y < 0: # if paddle goes below zero
                        self.player1.center_y = 0

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(20, 1))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(20, 1))

    def on_touch_move(self, touch):
        #if touch.x < self.width / 3:
        #    self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    def on_press_button(self):
        print('You pressed the button!')
        print(self.height, self.width)


class PongApp(App):
    def build(self):
        print("DMM")
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()