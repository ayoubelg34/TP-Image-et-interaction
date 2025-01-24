from PongGame import PongGame
from HandTracker import HandTracker
from Ball import Ball

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self, target_y, screen_height):
        self.y = max(0, min(target_y - self.height // 2, screen_height - self.height))

    def draw(self, frame, color):
        cv2.rectangle(
            frame,
            (self.x, self.y),
            (self.x + self.width, self.y + self.height),
            color,
            -1
        )