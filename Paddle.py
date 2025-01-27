import cv2

class Paddle:
    def __init__(self, x, y, width, height):
        """
        Initialise une raquette.
        :param x: Position en x de la raquette.
        :param y: Position en y de la raquette.
        :param width: Largeur de la raquette.
        :param height: Hauteur de la raquette.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self, position, screen_height):
        """
        Met à jour la position verticale de la raquette en fonction de la main détectée.
        """
        self.y = position - self.height // 2
        # S'assurer que la raquette reste dans l'écran
        self.y = max(0, min(self.y, screen_height - self.height))

    def draw(self, frame, color=(255, 0, 0)):
        """
        Dessine la raquette sur l'image.
        """
        top_left = (self.x, self.y)
        bottom_right = (self.x + self.width, self.y + self.height)

        # Dessiner un rectangle plein
        cv2.rectangle(frame, top_left, bottom_right, color, -1)
        # Bordure
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 0), 2)
