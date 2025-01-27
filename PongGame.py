import cv2
import numpy as np

from Ball import Ball
from Paddle import Paddle
from HandTracker import HandTracker
from BonusMalus import BonusMalus

class PongGame:
    def __init__(self, width, height):
        """
        Gère la logique principale du jeu Pong.
        """
        self.width = width
        self.height = height

        # Initialisation de la balle
        self.ball = Ball((width // 2, height // 2), (7, 7), 8)

        # Initialisation des raquettes
        self.left_paddle = Paddle(0, height // 2 - 50, 10, 100)
        self.right_paddle = Paddle(width - 10, height // 2 - 50, 10, 100)

        # Tracker de mains
        self.hand_tracker = HandTracker()

        # Gestion bonus/malus
        self.bonus_malus = BonusMalus(width, height)

        # Scores
        self.score_left = 0
        self.score_right = 0

        # Compteur pour déclencher spawn bonus/malus et augmentation de vitesse
        self.exchange_count = 0

    def update(self, hand_positions):
        """
        Met à jour l'état du jeu (raquettes, balle, score, bonus/malus, etc.)
        """
        # Mise à jour des raquettes via les positions de mains
        if hand_positions["Left"] is not None:
            self.left_paddle.update(hand_positions["Left"], self.height)
        if hand_positions["Right"] is not None:
            self.right_paddle.update(hand_positions["Right"], self.height)

        # Mise à jour de la balle
        self.ball.update(self.ball.speed_factor, self.width, self.height)

        # Vérifier si un point est marqué
        if self.ball.position[0] < 0:  # Balle sortie à gauche
            self.score_right += 1
            print(f"Point pour le joueur de droite ! Score : {self.score_right}")
            self.reset_ball(direction=1)
            return
        elif self.ball.position[0] > self.width:  # Balle sortie à droite
            self.score_left += 1
            print(f"Point pour le joueur de gauche ! Score : {self.score_left}")
            self.reset_ball(direction=-1)
            return

        # Vérifier les collisions avec les raquettes
        collision = False
        if self.ball.check_collision_with_paddle(self.left_paddle):
            print("Collision avec la raquette gauche.")
            self.exchange_count += 1
            collision = True
        elif self.ball.check_collision_with_paddle(self.right_paddle):
            print("Collision avec la raquette droite.")
            self.exchange_count += 1
            collision = True

        # Tous les 3 échanges, on fait apparaître un nouveau bonus/malus
        if collision and self.exchange_count % 3 == 0 and not self.bonus_malus.is_active():
            print(f"Génération d'un bonus ou d'un malus après {self.exchange_count} échanges.")
            self.bonus_malus.spawn_bonus_malus()

        # Augmentation de la vitesse de la balle tous les 4 échanges
        if collision and self.exchange_count % 4 == 0:
            self.ball.speed_factor *= 1.15  # on peut adapter ce facteur
            print(f"Vitesse de la balle augmentée : facteur = {self.ball.speed_factor}")

        # Vérifier la collision de la balle avec un éventuel bonus/malus
        self.bonus_malus.check_collision(self.ball, self.left_paddle, self.right_paddle)

    def reset_ball(self, direction):
        """
        Réinitialise la position et la vitesse de la balle après un point.
        Et réinitialise la taille des raquettes.
        """
        self.ball.position = np.array([self.width // 2, self.height // 2], dtype=float)
        self.ball.velocity = np.array([direction * 7, 7], dtype=float)
        self.ball.speed_factor = 1.0
        self.exchange_count = 0

        # Remise à la taille initiale des raquettes
        self.left_paddle.height = 100
        self.right_paddle.height = 100
        print("Balle et raquettes réinitialisées.")

    def draw(self, frame):
        """
        Dessine tous les éléments du jeu sur la frame donnée.
        """
        # Dessin de la balle
        self.ball.draw(frame)

        # Dessin des raquettes
        self.left_paddle.draw(frame, color=(0, 255, 0))   # raquette gauche (vert)
        self.right_paddle.draw(frame, color=(255, 0, 0))  # raquette droite (bleu)

        # Dessin des bonus/malus
        self.bonus_malus.draw(frame)

        # Afficher les scores
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f"Score Gauche: {self.score_left}",
                    (50, 50), font, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"Score Droit: {self.score_right}",
                    (self.width - 300, 50), font, 1, (255, 255, 255), 2)
