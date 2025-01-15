from Ball import Ball
from Paddle import Paddle
from HandTracker import HandTracker
import numpy as np
import cv2

class PongGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ball = Ball((width // 2, height // 2), (7, 7), 8)
        self.left_paddle = Paddle(0, height // 2 - 50, 10, 100)
        self.right_paddle = Paddle(width - 10, height // 2 - 50, 10, 100)
        self.hand_tracker = HandTracker()
        self.score_left = 0
        self.score_right = 0
        self.exchange_count = 0  # Counter for exchanges

    def update(self, hand_positions):
        if hand_positions["Left"] is not None:
            self.left_paddle.update(hand_positions["Left"], self.height)
        if hand_positions["Right"] is not None:
            self.right_paddle.update(hand_positions["Right"], self.height)

        self.ball.update(1, self.width, self.height)
        
        if self.ball.check_collision_with_paddle(self.left_paddle) or self.ball.check_collision_with_paddle(self.right_paddle):
            self.exchange_count += 1
            if self.exchange_count % 2 == 0:
                self.ball.speed_factor *= 1.2  # Increase speed factor every 2 exchanges

        if self.ball.position[0] < 0:
            self.score_right += 1
            self.reset_ball(direction=1)
        elif self.ball.position[0] > self.width:
            self.score_left += 1
            self.reset_ball(direction=-1)

    def reset_ball(self, direction):
        self.ball.position = np.array([self.width // 2, self.height // 2], dtype=float)
        self.ball.velocity = np.array([direction * 7, 7], dtype=float)
        self.ball.speed_factor = 1.0  # Reset speed factor
        self.exchange_count = 0  # Reset exchange count

    def draw(self, frame):
        self.left_paddle.draw(frame, (0, 255, 0))
        self.right_paddle.draw(frame, (0, 0, 255))
        self.ball.draw(frame)

        cv2.putText(
            frame,
            f"{self.score_left} - {self.score_right}",
            (self.width // 2 - 50, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )