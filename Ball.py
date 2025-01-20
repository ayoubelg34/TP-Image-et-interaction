import cv2
import mediapipe as mp
import numpy as np

class Ball:
    def __init__(self, position, velocity, size):
        """
        Initialise une instance de la balle.

        :param position: Position initiale de la balle (tuple ou liste de deux valeurs).
        :param velocity: Vitesse initiale de la balle (tuple ou liste de deux valeurs).
        :param size: Taille (rayon) de la balle en pixels.
        """
        self.position = np.array(position, dtype=float)  # Position actuelle de la balle (en coordonnées x, y).
        self.velocity = np.array(velocity, dtype=float)  # Vitesse actuelle de la balle (composantes x, y).
        self.size = size  # Rayon de la balle.
        self.speed_factor = 1.0  # Facteur de vitesse pour ajuster la rapidité de la balle.

    def update(self, dt, screen_width, screen_height):
        """
        Met à jour la position de la balle en fonction de la vitesse et du temps écoulé.

        :param dt: Temps écoulé (en secondes) depuis la dernière mise à jour.
        :param screen_width: Largeur de l'écran (en pixels).
        :param screen_height: Hauteur de l'écran (en pixels).
        """
        # Met à jour la position en utilisant la vitesse et le facteur de vitesse.
        self.position += self.velocity * dt * self.speed_factor

        # Gérer les rebonds de la balle sur les bords supérieur et inférieur de l'écran.
        if self.position[1] <= 0 or self.position[1] >= screen_height - self.size:
            self.velocity[1] *= -1  # Inverse la composante verticale de la vitesse (rebond).

    def check_collision_with_paddle(self, paddle):
        """
        Vérifie si la balle entre en collision avec une raquette.

        :param paddle: Objet représentant une raquette, avec des attributs `x`, `y`, `width` et `height`.
        :return: True si une collision est détectée, False sinon.
        """
        # Vérifie si la balle est dans la zone de collision de la raquette.
        if (paddle.x <= self.position[0] <= paddle.x + paddle.width and
                paddle.y <= self.position[1] <= paddle.y + paddle.height):
            self.velocity[0] *= -1  # Inverse la composante horizontale de la vitesse (rebond).
            return True  # Collision détectée.
        return False  # Pas de collision.

    def draw(self, frame):
        """
        Dessine la balle sur le cadre donné.

        :param frame: Image (frame) sur laquelle dessiner la balle (matrice numpy).
        """
        # Dessine un cercle représentant la balle, avec sa position actuelle et sa taille.
        cv2.circle(frame, (int(self.position[0]), int(self.position[1])), self.size, (255, 255, 255), -1)
