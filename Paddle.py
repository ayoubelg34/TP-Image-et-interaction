class Paddle:
    def __init__(self, x, y, width, height):
        """
        Initialise une raquette.
        :param x: Position horizontale de la raquette (gauche ou droite).
        :param y: Position verticale de la raquette (centre initial).
        :param width: Largeur de la raquette.
        :param height: Hauteur de la raquette.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self, position, screen_height):
        """
        Met à jour la position verticale de la raquette.
        :param position: Nouvelle position verticale (en pixels).
        :param screen_height: Hauteur de l'écran (pour éviter de dépasser les limites).
        """
        # Centrer la raquette autour de la nouvelle position
        self.y = position - self.height // 2

        # Empêcher la raquette de sortir de l'écran
        self.y = max(0, min(self.y, screen_height - self.height))

    def draw(self, frame, color):
        """
        Dessine la raquette sur le cadre.
        :param frame: Image (frame) sur laquelle dessiner la raquette.
        :param color: Couleur de la raquette (tuple BGR).
        """
        import cv2
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), color, -1)

