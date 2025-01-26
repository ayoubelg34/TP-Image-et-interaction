from Ball import Ball
from Paddle import Paddle
from HandTracker import HandTracker
import numpy as np
import cv2

class PongGame:
    def __init__(self, width, height):
        print("Initialisation de PongGame...")

        self.width = width
        self.height = height

        # Initialisation des éléments du jeu
        try:
            print("Initialisation de la balle...")
            self.ball = Ball((width // 2, height // 2), (7, 7), 8)
            print("Balle initialisée.")
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la balle : {e}")

        try:
            print("Initialisation des raquettes...")
            self.left_paddle = Paddle(0, height // 2 - 50, 10, 100)
            self.right_paddle = Paddle(width - 10, height // 2 - 50, 10, 100)
            print("Raquettes initialisées.")
        except Exception as e:
            print(f"Erreur lors de l'initialisation des raquettes : {e}")

        try:
            print("Initialisation du tracker de mains...")
            self.hand_tracker = HandTracker()
            print("Tracker de mains initialisé.")
        except Exception as e:
            print(f"Erreur lors de l'initialisation du tracker de mains : {e}")

        # Initialisation des scores
        self.score_left = 0
        self.score_right = 0
        print("PongGame initialisé avec succès.")


    def update(self, hand_positions):
        """
        Met à jour l'état du jeu (positions des raquettes, balle, score).

        :param hand_positions: Positions des mains détectées, données sous forme d'un dictionnaire {"Left": y, "Right": y}.
        """
        # Mettre à jour la position de la raquette gauche si une main gauche est détectée.
        if hand_positions["Left"] is not None:
            self.left_paddle.update(hand_positions["Left"], self.height)

        # Mettre à jour la position de la raquette droite si une main droite est détectée.
        if hand_positions["Right"] is not None:
            self.right_paddle.update(hand_positions["Right"], self.height)

        # Mettre à jour la position de la balle.
        self.ball.update(1, self.width, self.height)

        # Vérifier les collisions de la balle avec les raquettes.
        if (self.ball.check_collision_with_paddle(self.left_paddle) or
                self.ball.check_collision_with_paddle(self.right_paddle)):
            self.exchange_count += 1  # Incrémenter le compteur d'échanges.
            if self.exchange_count % 2 == 0:
                self.ball.speed_factor *= 1.2  # Augmenter la vitesse tous les 2 échanges.

        # Vérifier si la balle sort des limites pour marquer un point.
        if self.ball.position[0] < 0:
            self.score_right += 1  # Point pour le joueur droit.
            self.reset_ball(direction=1)  # Réinitialiser la balle en direction du joueur droit.
        elif self.ball.position[0] > self.width:
            self.score_left += 1  # Point pour le joueur gauche.
            self.reset_ball(direction=-1)  # Réinitialiser la balle en direction du joueur gauche.

    def reset_ball(self, direction):
        """
        Réinitialise la position et la vitesse de la balle après un point.

        :param direction: Direction initiale de la balle après réinitialisation (1 pour droite, -1 pour gauche).
        """
        self.ball.position = np.array([self.width // 2, self.height // 2], dtype=float)
        self.ball.velocity = np.array([direction * 7, 7], dtype=float)
        self.ball.speed_factor = 1.0  # Réinitialiser le facteur de vitesse.
        self.exchange_count = 0  # Réinitialiser le compteur d'échanges.

    def draw(self, frame):
        """
        Dessine les éléments du jeu sur le cadre donné.

        :param frame: Image (matrice numpy) sur laquelle dessiner les éléments du jeu.
        """
        # Dessiner les raquettes (gauche et droite).
        self.left_paddle.draw(frame, (0, 255, 0))  # Vert pour la raquette gauche.
        self.right_paddle.draw(frame, (0, 0, 255))  # Rouge pour la raquette droite.

        # Dessiner la balle.
        self.ball.draw(frame)

        # Afficher les scores au centre supérieur de l'écran.
        cv2.putText(
            frame,
            f"{self.score_left} - {self.score_right}",  # Format des scores.
            (self.width // 2 - 50, 30),  # Position du texte.
            cv2.FONT_HERSHEY_SIMPLEX,  # Police du texte.
            1,  # Taille du texte.
            (255, 255, 255),  # Couleur blanche.
            2  # Épaisseur du texte.
        )
