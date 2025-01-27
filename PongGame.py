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
        self.ball = Ball(position=(width // 2, height // 2),
                         velocity=(7, 7),
                         size=8)

        # Raquettes
        self.left_paddle = Paddle(0, height // 2 - 50, 10, 100)
        self.right_paddle = Paddle(width - 10, height // 2 - 50, 10, 100)

        # Tracker de mains
        self.hand_tracker = HandTracker()

        # Bonus/Malus
        self.bonus_malus = BonusMalus(width, height)

        # Scores
        self.score_left = 0
        self.score_right = 0

        # Compte le nombre d'échanges (collisions balle-raquette)
        self.exchange_count = 0

        # Pour gérer la fin de partie
        self.game_over = False
        self.winner = None

    def update(self, hand_positions):
        """
        Met à jour l'état du jeu (raquettes, balle, bonus/malus, scores).
        """
        if self.game_over:
            return  # Ne plus rien faire si le jeu est terminé

        # Mise à jour des raquettes si la main est détectée
        if hand_positions["Left"] is not None:
            self.left_paddle.update(hand_positions["Left"], self.height)
        if hand_positions["Right"] is not None:
            self.right_paddle.update(hand_positions["Right"], self.height)

        # Mise à jour de la balle
        self.ball.update(self.ball.speed_factor, self.width, self.height)

        # Vérifier si un point est marqué
        # Balle sortie à gauche
        if self.ball.position[0] < 0:
            self.score_right += 1
            print(f"Point pour le joueur de droite ! Score : {self.score_right}")
            self.check_winner()
            if not self.game_over:
                self.reset_ball(direction=1)
            return

        # Balle sortie à droite
        elif self.ball.position[0] > self.width:
            self.score_left += 1
            print(f"Point pour le joueur de gauche ! Score : {self.score_left}")
            self.check_winner()
            if not self.game_over:
                self.reset_ball(direction=-1)
            return

        # Vérifier les collisions avec les raquettes
        collision = False
        if self.ball.check_collision_with_paddle(self.left_paddle):
            collision = True
        elif self.ball.check_collision_with_paddle(self.right_paddle):
            collision = True

        # S'il y a eu collision (un échange)
        if collision:
            # Incrémente le compteur d'échanges
            self.exchange_count += 1

            # À CHAQUE échange, on :
            # 1) Fait apparaître un nouveau bonus/malus (si aucun actif)
            self.bonus_malus.spawn_bonus_malus()

            # 2) Augmente la vitesse de la balle de 5%
            self.ball.speed_factor *= 1.05
            print(f"Vitesse de la balle augmentée : facteur = {self.ball.speed_factor}")

        # Vérifier la collision de la balle avec un éventuel bonus/malus
        self.bonus_malus.check_collision(self.ball, self.left_paddle, self.right_paddle)

    def check_winner(self):
        """
        Vérifie si un des joueurs a atteint 5 points.
        Si oui, on arrête le jeu.
        """
        if self.score_left >= 5:
            self.game_over = True
            self.winner = "Gauche"
            print("Le joueur de gauche remporte la partie !")
        elif self.score_right >= 5:
            self.game_over = True
            self.winner = "Droite"
            print("Le joueur de droite remporte la partie !")

    def reset_ball(self, direction):
        """
        Réinitialise la position et la vitesse de la balle après un point.
        Remet les raquettes à leur taille initiale.
        """
        self.ball.position = np.array([self.width // 2, self.height // 2], dtype=float)
        self.ball.velocity = np.array([direction * 7, 7], dtype=float)
        self.ball.speed_factor = 1.0
        self.exchange_count = 0

        self.left_paddle.height = 100
        self.right_paddle.height = 100
        print("Balle et raquettes réinitialisées.")

    def draw(self, frame):
        """
        Dessine tous les éléments du jeu sur la frame.
        """
        # Dessin de la balle
        self.ball.draw(frame)

        # Dessin des raquettes
        self.left_paddle.draw(frame, color=(0, 255, 0))    # raquette gauche (vert)
        self.right_paddle.draw(frame, color=(255, 0, 0))   # raquette droite (bleu)

        # Dessin bonus/malus
        self.bonus_malus.draw(frame)

        # Afficher les scores
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,
                    f"Score Gauche: {self.score_left}",
                    (50, 50), font, 1, (255, 255, 255), 2)
        cv2.putText(frame,
                    f"Score Droit: {self.score_right}",
                    (self.width - 300, 50), font, 1, (255, 255, 255), 2)

        # Si le jeu est terminé, afficher un message de fin
        if self.game_over and self.winner:
            cv2.putText(frame,
                        f"Le joueur {self.winner} gagne!",
                        (int(self.width / 2 - 150), int(self.height / 2)),
                        font, 1.2, (0, 255, 255), 3)
