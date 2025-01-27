import cv2
import numpy as np

class Ball:
    def __init__(self, position, velocity, size):
        """
        Initialise une instance de la balle.

        :param position: Position initiale de la balle (tuple ou liste de deux valeurs).
        :param velocity: Vitesse initiale de la balle (tuple ou liste de deux valeurs).
        :param size: Taille (rayon) de la balle en pixels.
        """
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.size = size
        self.speed_factor = 1.0

    def update(self, speed_factor, screen_width, screen_height):
        """
        Met à jour la position de la balle.
        :param speed_factor: Facteur de vitesse pour la balle.
        :param screen_width: Largeur de l'écran.
        :param screen_height: Hauteur de l'écran.
        """
        self.position[0] += self.velocity[0] * speed_factor
        self.position[1] += self.velocity[1] * speed_factor

        # Rebondir sur les bords supérieur et inférieur de l'écran
        if self.position[1] <= 0 or self.position[1] >= screen_height - self.size:
            self.velocity[1] *= -1

    def check_collision_with_paddle(self, paddle):
        """
        Vérifie si la balle entre en collision avec la raquette donnée.
        Renvoie True s'il y a collision, False sinon.
        """
        print(
            f"Vérification collision : Balle à ({self.position[0]}, {self.position[1]}), "
            f"Raquette ({paddle.x}, {paddle.y}, {paddle.width}, {paddle.height})"
        )
        if (
            paddle.x <= self.position[0] <= paddle.x + paddle.width and
            paddle.y <= self.position[1] <= paddle.y + paddle.height
        ):
            self.velocity[0] *= -1
            print("Collision détectée avec une raquette.")
            return True
        return False

    def draw(self, frame):
        """
        Dessine la balle avec un dégradé et une ombre.
        """
        center = (int(self.position[0]), int(self.position[1]))

        # Ombre légère
        shadow_offset = 3
        cv2.circle(frame, (center[0] + shadow_offset, center[1] + shadow_offset),
                   self.size, (50, 50, 50), -1)

        # Dégradé radial (blanc vers bleu clair)
        for i in range(self.size, 0, -1):
            color_intensity = 255 - int((i / self.size) * 255)
            color = (255, color_intensity, color_intensity)  # Dégradé de blanc à bleu clair
            cv2.circle(frame, center, i, color, -1)
