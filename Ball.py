import cv2
import mediapipe as mp
import numpy as np

class Ball:
    def __init__(self, position, velocity, size):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.size = size

    def update(self, dt, screen_width, screen_height):
        self.position += self.velocity * dt

        # Gérer les rebonds avec les bords supérieur et inférieur
        if self.position[1] <= 0 or self.position[1] >= screen_height - self.size:
            self.velocity[1] *= -1

    def check_collision_with_paddle(self, paddle):
        if (paddle.x <= self.position[0] <= paddle.x + paddle.width and
                paddle.y <= self.position[1] <= paddle.y + paddle.height):
            self.velocity[0] *= -1

    def draw(self, frame):
        cv2.circle(frame, (int(self.position[0]), int(self.position[1])), self.size, (255, 255, 255), -1)
