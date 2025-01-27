import cv2

class Paddle:
    def __init__(self, x, y, width, height):
        """
        Initialise une raquette.
        :param x: Position x de la raquette.
        :param y: Position y de la raquette.
        :param width: Largeur.
        :param height: Hauteur.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self, position, screen_height):
        """
        Déplace la raquette en fonction de la coordonnée y détectée.
        """
        self.y = position - self.height // 2
        # Empêche la raquette de sortir de l'écran
        self.y = max(0, min(self.y, screen_height - self.height))

    def draw(self, frame, color=(255, 0, 0)):
        """
        Dessine la raquette sur la frame.
        """
        top_left = (self.x, self.y)
        bottom_right = (self.x + self.width, self.y + self.height)

        # Remplissage principal
        cv2.rectangle(frame, top_left, bottom_right, color, -1)

        # Bordure (effet 3D simple)
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 0), 2)
