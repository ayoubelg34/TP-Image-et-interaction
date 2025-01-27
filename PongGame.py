import cv2
import numpy as np

from Ball import Ball
from Paddle import Paddle
from HandTracker import HandTracker
from BonusMalus import BonusMalus

class PongGame:
    def __init__(self, width, height):
        """
        Gestion principale du jeu Pong.
        """
        self.width = width
        self.height = height

        # Création de la balle
        self.ball = Ball((width // 2, height // 2), (7, 7), 8)

        # Création des raquettes (gauche / droite)
        self.left_paddle = Paddle(0, height // 2 - 50, 10, 100)
        self.right_paddle = Paddle(width - 10, height // 2 - 50, 10, 100)

        # Tracker de mains
        self.hand_tracker = HandTracker()

        # Système de bonus/malus
        self.bonus_malus = BonusMalus(width, height)

        # Scores des deux joueurs
        self.score_left = 0
        self.score_right = 0

        # Permet de détecter la fin de partie
        self.game_over = False
        self.winner = None

        # Compte le nombre d'échanges (facultatif si on veut se baser dessus)
        self.exchange_count = 0

    def update(self, hand_positions):
        """
        Met à jour l'état du jeu (positions des raquettes, balle, bonus/malus).
        """
        if self.game_over:
            return

        # Mise à jour des raquettes selon la position verticale détectée
        if hand_positions["Left"] is not None:
            self.left_paddle.update(hand_positions["Left"], self.height)
        if hand_positions["Right"] is not None:
            self.right_paddle.update(hand_positions["Right"], self.height)

        # Déplacement de la balle
        self.ball.update(self.ball.speed_factor, self.width, self.height)

        # Vérifier si la balle sort à gauche (point pour la droite)
        if self.ball.position[0] < 0:
            self.score_right += 1
            print(f"Point pour la droite ! Score: {self.score_right}")
            self.reset_ball(direction=1)
            self.check_winner()
            return

        # Vérifier si la balle sort à droite (point pour la gauche)
        if self.ball.position[0] > self.width:
            self.score_left += 1
            print(f"Point pour la gauche ! Score: {self.score_left}")
            self.reset_ball(direction=-1)
            self.check_winner()
            return

        # Vérifier collisions balle-raquettes
        collision = False
        if self.ball.check_collision_with_paddle(self.left_paddle):
            collision = True
        elif self.ball.check_collision_with_paddle(self.right_paddle):
            collision = True

        # S'il y a collision avec une raquette
        if collision:
            # Augmenter la vitesse de la balle de 10%
            self.ball.speed_factor *= 1.1
            self.exchange_count += 1
            print(f"Échange n°{self.exchange_count} : vitesse balle={self.ball.speed_factor:.2f}")

            # Générer un nouveau bonus/malus (dans la limite de 5)
            self.bonus_malus.spawn_item()

        # Vérifier collisions balle-bonus/malus
        self.bonus_malus.check_collision(self.ball, self.left_paddle, self.right_paddle)

    def reset_ball(self, direction):
        """
        Réinitialise la balle au centre et remet les raquettes à la taille normale.
        """
        self.ball.position = np.array([self.width // 2, self.height // 2], dtype=float)
        self.ball.velocity = np.array([direction * 7, 7], dtype=float)
        self.ball.speed_factor = 1.0
        self.exchange_count = 0

        # Raquettes redeviennent taille normale
        self.left_paddle.height = 100
        self.right_paddle.height = 100

        print("Balle et raquettes réinitialisées.")

    def check_winner(self):
        """
        Vérifie si l'un des deux joueurs a atteint 5 points.
        Si oui, on arrête le jeu et on stocke le vainqueur.
        """
        if self.score_left >= 5:
            self.game_over = True
            self.winner = "Gauche"
        elif self.score_right >= 5:
            self.game_over = True
            self.winner = "Droite"

    def draw(self, frame):
        """
        Dessine tous les éléments du jeu (balle, raquettes, bonus/malus, scores).
        Si le jeu est terminé, affiche un écran de fin.
        """
        if not self.game_over:
            # Dessin de la balle
            self.ball.draw(frame)

            # Dessin des raquettes
            self.left_paddle.draw(frame, color=(0, 255, 0))   # raquette gauche (vert)
            self.right_paddle.draw(frame, color=(255, 0, 0))  # raquette droite (bleu)

            # Dessin des bonus/malus
            self.bonus_malus.draw(frame)

            # Afficher les scores
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, f"Score Gauche: {self.score_left}", (50, 50), font, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"Score Droit: {self.score_right}", (self.width - 300, 50), font, 1, (255, 255, 255), 2)
        else:
            # Écran de fin
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = f"Le vainqueur est : {self.winner} !"
            text_size, _ = cv2.getTextSize(text, font, 2, 3)
            text_x = (self.width - text_size[0]) // 2
            text_y = (self.height // 2)

            cv2.putText(frame, text, (text_x, text_y), font, 2, (0, 255, 0), 3)

