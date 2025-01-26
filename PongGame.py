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
        self.bonus_image = cv2.imread("assets/star.png", cv2.IMREAD_UNCHANGED)  # Image d'étoile
        self.malus_image = cv2.imread("assets/bomb.png", cv2.IMREAD_UNCHANGED)  # Image de bombe

        # Redimensionner les images pour qu'elles soient adaptées au terrain
        if self.bonus_image is not None:
            self.bonus_image = cv2.resize(self.bonus_image, (50, 50), interpolation=cv2.INTER_AREA)
        if self.malus_image is not None:
            self.malus_image = cv2.resize(self.malus_image, (50, 50), interpolation=cv2.INTER_AREA)

        # Initialiser les autres composants du jeu
        self.ball = Ball((width // 2, height // 2), (7, 7), 8)
        self.left_paddle = Paddle(0, height // 2 - 50, 10, 100)
        self.right_paddle = Paddle(width - 10, height // 2 - 50, 10, 100)
        self.hand_tracker = HandTracker()

        # Scores et états de bonus/malus
        self.score_left = 0
        self.score_right = 0
        self.bonus_active = False
        self.malus_active = False
        self.bonus_position = None
        self.malus_position = None
        self.exchange_count = 0  # Compteur d'échanges


    def update(self, hand_positions):
        """
        Met à jour l'état du jeu (raquettes, balle, score, bonus/malus).
        """
        # Mettre à jour les raquettes en fonction des mains
        if hand_positions["Left"] is not None:
            self.left_paddle.update(hand_positions["Left"], self.height)
        if hand_positions["Right"] is not None:
            self.right_paddle.update(hand_positions["Right"], self.height)

        # Mettre à jour la position de la balle
        self.ball.update(self.ball.speed_factor, self.width, self.height)

        # Vérifier si la balle touche les murs gauche ou droit (point marqué)
        if self.ball.position[0] < 0:  # Mur gauche
            self.score_right += 1
            print(f"Point pour le joueur de droite ! Score : {self.score_right}")
            self.reset_ball(direction=1)  # Réinitialiser la balle vers la droite
        elif self.ball.position[0] > self.width:  # Mur droit
            self.score_left += 1
            print(f"Point pour le joueur de gauche ! Score : {self.score_left}")
            self.reset_ball(direction=-1)  # Réinitialiser la balle vers la gauche

        # Vérifier les collisions entre la balle et les raquettes
        if self.ball.check_collision_with_paddle(self.left_paddle):
            print("Collision avec la raquette gauche.")
            self.exchange_count += 1
        elif self.ball.check_collision_with_paddle(self.right_paddle):
            print("Collision avec la raquette droite.")
            self.exchange_count += 1

        # Tous les 3 échanges, générer un bonus/malus supplémentaire
        if self.exchange_count % 3 == 0 and (not self.bonus_active or not self.malus_active) and self.exchange_count > 0:
            print("Génération d'un bonus ou d'un malus après 3 échanges.")
            self.spawn_bonus_malus()

        # Tous les 4 échanges, augmenter la vitesse de la balle
        if self.exchange_count % 4 == 0 and self.exchange_count > 0:
            self.ball.speed_factor *= 1.2
            print(f"Vitesse de la balle augmentée : facteur = {self.ball.speed_factor}")

        # Vérifier si la balle touche un bonus ou un malus
        self.check_bonus_malus_collision()

        
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
        Génère un bonus ou un malus aléatoirement.
        """
        import random
        choice = random.random()
        if choice < 0.5:  # 50% de chance pour un bonus
            self.bonus_active = True
            self.bonus_position = (self.width // 2, random.randint(50, self.height - 50))
            print(f"Bonus généré à la position : {self.bonus_position}")
        else:  # 50% de chance pour un malus
            self.malus_active = True
            self.malus_position = (self.width // 2, random.randint(50, self.height - 50))
            print(f"Malus généré à la position : {self.malus_position}")

    
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
        """
        Dessine une image avec transparence sur le frame.
        :param frame: Image sur laquelle dessiner.
        :param image: Image à dessiner (avec un canal alpha pour la transparence).
        :param position: Tuple (x, y) pour la position de l'image.
        """
        x, y = position
        h, w, _ = image.shape

        # Découper la région où dessiner l'image
        overlay = frame[y:y+h, x:x+w]
        alpha_mask = image[:, :, 3] / 255.0
        for c in range(0, 3):
            overlay[:, :, c] = (1.0 - alpha_mask) * overlay[:, :, c] + alpha_mask * image[:, :, c]
        frame[y:y+h, x:x+w] = overlay

    def draw_bonus_malus(self, frame):
        """
        Dessine les bonus et malus sur le terrain avec des images.
        """
        if self.bonus_active and self.bonus_position:
            x, y = self.bonus_position
            h, w, _ = self.bonus_image.shape
            # Assurez-vous que l'image reste dans les limites de l'écran
            if 0 <= y - h // 2 < self.height and 0 <= x - w // 2 < self.width:
                self.draw_transparent_image(frame, self.bonus_image, (x - w // 2, y - h // 2))

        if self.malus_active and self.malus_position:
            x, y = self.malus_position
            h, w, _ = self.malus_image.shape
            # Assurez-vous que l'image reste dans les limites de l'écran
            if 0 <= y - h // 2 < self.height and 0 <= x - w // 2 < self.width:
                self.draw_transparent_image(frame, self.malus_image, (x - w // 2, y - h // 2))
    
    