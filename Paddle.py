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
        Met à jour la position de la raquette en se basant sur
        la position verticale détectée (ex: y de la main).
        """
        self.y = position - self.height // 2
        self.y = max(0, min(self.y, screen_height - self.height))

    def draw(self, frame, color=(255, 0, 0)):
        """
        Dessine la raquette sur la frame.
        """
        top_left = (self.x, self.y)
        bottom_right = (self.x + self.width, self.y + self.height)

        # Remplissage principal
        cv2.rectangle(frame, top_left, bottom_right, color, -1)

        # Bordure pour donner un effet "3D"
        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 0), 2)
