import cv2

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self, position, screen_height):
        self.y = position - self.height // 2
        self.y = max(0, min(self.y, screen_height - self.height))

    def draw(self, frame, color):
        # Dessiner un rectangle arrondi pour la raquette
        top_left = (self.x, self.y)
        bottom_right = (self.x + self.width, self.y + self.height)

        # Remplissage principal
        cv2.rectangle(frame, top_left, bottom_right, color, -1)

        # Bordure pour donner un effet "3D"
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 0), 2)

        # Ombre (ajouter un rectangle légèrement
