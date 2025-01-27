from Ball import Ball
from Paddle import Paddle
from HandTracker import HandTracker
import numpy as np
import cv2

class PongGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Charger les images pour le bonus et le malus
        self.bonus_image = cv2.imread("assets/star.png", cv2.IMREAD_UNCHANGED)
        if self.bonus_image is None:
            print("Erreur : Impossible de charger l'image star.png.")
        else:
            self.bonus_image = cv2.resize(self.bonus_image, (50, 50), interpolation=cv2.INTER_AREA)

        self.malus_image = cv2.imread("assets/bomb.png", cv2.IMREAD_UNCHANGED)
        if self.malus_image is None:
            print("Erreur : Impossible de charger l'image bomb.png.")
        else:
            self.malus_image = cv2.resize(self.malus_image, (50, 50), interpolation=cv2.INTER_AREA)

        # Autres initialisations
        self.ball = Ball((width // 2, height // 2), (7, 7), 8)
        self.left_paddle = Paddle(0, height // 2 - 50, 10, 100)
        self.right_paddle = Paddle(width - 10, height // 2 - 50, 10, 100)
        self.hand_tracker = HandTracker()

        # Scores et états
        self.score_left = 0
        self.score_right = 0
        self.bonus_active = False
        self.malus_active = False
        self.bonus_position = None
        self.malus_position = None
        self.exchange_count = 0



    def update(self, hand_positions):
        """
        Met à jour l'état du jeu (raquettes, balle, score, bonus/malus).
        """
        if hand_positions["Left"] is not None:
            self.left_paddle.update(hand_positions["Left"], self.height)
        if hand_positions["Right"] is not None:
            self.right_paddle.update(hand_positions["Right"], self.height)

        # Mise à jour de la balle
        self.ball.update(self.ball.speed_factor, self.width, self.height)

        # Vérifier si un point est marqué
        if self.ball.position[0] < 0:
            self.score_right += 1
            self.reset_ball(direction=1)
            return
        elif self.ball.position[0] > self.width:
            self.score_left += 1
            self.reset_ball(direction=-1)
            return

        # Collision avec les raquettes
        if self.ball.check_collision_with_paddle(self.left_paddle):
            self.exchange_count += 1
        elif self.ball.check_collision_with_paddle(self.right_paddle):
            self.exchange_count += 1

        # Gestion des bonus/malus
        if self.exchange_count % 3 == 0 and self.exchange_count > 0 and not (self.bonus_active or self.malus_active):
            self.spawn_bonus_malus()

        if self.exchange_count % 4 == 0 and self.exchange_count > 0:
            self.ball.speed_factor *= 1.01


        
    def reset_ball(self, direction):
        """
        Réinitialise la position et la vitesse de la balle après un point.
        """
        self.ball.position = np.array([self.width // 2, self.height // 2], dtype=float)
        self.ball.velocity = np.array([direction * 7, 7], dtype=float)
        self.ball.speed_factor = 1.0  # Réinitialiser le facteur de vitesse.
        self.exchange_count = 0  # Réinitialiser le compteur d'échanges.
        print("Balle réinitialisée au centre.")


    def draw(self, frame):
        self.left_paddle.draw(frame, (0, 255, 0))  # Vert
        self.right_paddle.draw(frame, (0, 0, 255))  # Rouge
        self.ball.draw(frame)  # Dessiner la balle
        self.draw_bonus_malus(frame)  # Dessiner les bonus/malus

        # Afficher les scores
        cv2.putText(frame, f"{self.score_left} - {self.score_right}",
                    (self.width // 2 - 50, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2)

    
    def spawn_bonus_malus(self):
        """
        Génère un bonus ou un malus aléatoirement si aucun n'est actif.
        """
        import random

        # Vérifier qu'aucun bonus/malus n'est déjà actif
        if self.bonus_active or self.malus_active:
            print("Un bonus ou un malus est déjà actif, aucune génération.")
            return

        # Décider aléatoirement entre bonus et malus
        choice = random.random()

        if choice < 0.5:  # Générer un bonus
            if self.bonus_image is not None:
                self.bonus_active = True
                self.bonus_position = (random.randint(50, self.width - 50), random.randint(50, self.height - 50))
                print(f"Bonus généré à la position : {self.bonus_position}")
            else:
                print("Erreur : L'image de bonus est manquante.")
        else:  # Générer un malus
            if self.malus_image is not None:
                self.malus_active = True
                self.malus_position = (random.randint(50, self.width - 50), random.randint(50, self.height - 50))
                print(f"Malus généré à la position : {self.malus_position}")
            else:
                print("Erreur : L'image de malus est manquante.")

    
    def check_bonus_malus_collision(self):
        """
        Vérifie si la balle touche un bonus ou un malus et applique l'effet correspondant.
        """
        if self.bonus_active and self.bonus_position:
            bonus_x, bonus_y = self.bonus_position
            if (bonus_x - 10 <= self.ball.position[0] <= bonus_x + 10 and
                    bonus_y - 10 <= self.ball.position[1] <= bonus_y + 10):
                # Collision avec un bonus
                self.bonus_active = False
                self.bonus_position = None
                if self.ball.velocity[0] > 0:  # La balle va vers la droite
                    self.right_paddle.height = int(self.right_paddle.height * 1.3)
                else:  # La balle va vers la gauche
                    self.left_paddle.height = int(self.left_paddle.height * 1.3)
                print("Bonus appliqué : raquette agrandie de 30%.")

        if self.malus_active and self.malus_position:
            malus_x, malus_y = self.malus_position
            if (malus_x - 10 <= self.ball.position[0] <= malus_x + 10 and
                    malus_y - 10 <= self.ball.position[1] <= malus_y + 10):
                # Collision avec un malus
                self.malus_active = False
                self.malus_position = None
                if self.ball.velocity[0] > 0:  # La balle va vers la droite
                    self.right_paddle.height = max(30, int(self.right_paddle.height * 0.5))
                else:  # La balle va vers la gauche
                    self.left_paddle.height = max(30, int(self.left_paddle.height * 0.5))
                print("Malus appliqué : raquette réduite de 50%.")

    def draw_transparent_image(self, frame, image, position):
        if image is None:
            print("Erreur : L'image fournie est 'None'.")
            return

        x, y = position
        h, w, _ = image.shape

        # S'assurer que la région ne dépasse pas les dimensions du frame
        if y + h > frame.shape[0] or x + w > frame.shape[1]:
            return  # Ne pas dessiner si cela dépasse les limites

        # Découper la région où dessiner l'image
        overlay = frame[y:y + h, x:x + w]
        alpha_mask = image[:, :, 3] / 255.0  # Canal alpha normalisé

        # Dessiner chaque canal (B, G, R)
        for c in range(0, 3):
            overlay[:, :, c] = (1.0 - alpha_mask) * overlay[:, :, c] + alpha_mask * image[:, :, c]

        frame[y:y + h, x:x + w] = overlay

    def draw_bonus_malus(self, frame):
        """
        Dessine les bonus et malus sur le terrain avec des images.
        """
        if self.bonus_active and self.bonus_position:
            if self.bonus_image is not None:  # Vérifiez si l'image est chargée
                x, y = self.bonus_position
                h, w, _ = self.bonus_image.shape
                if 0 <= y - h // 2 < self.height and 0 <= x - w // 2 < self.width:
                    self.draw_transparent_image(frame, self.bonus_image, (x - w // 2, y - h // 2))
            else:
                print("Erreur : Image de bonus non disponible.")

        if self.malus_active and self.malus_position:
            if self.malus_image is not None:  # Vérifiez si l'image est chargée
                x, y = self.malus_position
                h, w, _ = self.malus_image.shape
                if 0 <= y - h // 2 < self.height and 0 <= x - w // 2 < self.width:
                    self.draw_transparent_image(frame, self.malus_image, (x - w // 2, y - h // 2))
            else:
                print("Erreur : Image de malus non disponible.")
