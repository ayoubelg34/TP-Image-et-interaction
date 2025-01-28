import cv2
import numpy as np
import random

class BonusMalus:
    """
    Gère l'apparition, l'affichage et les collisions de plusieurs bonus et malus.
    Un bonus agrandit la raquette de 30%, un malus la réduit de 50%.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Chargement des images
        self.bonus_image = cv2.imread("assets/star.png", cv2.IMREAD_UNCHANGED)
        if self.bonus_image is not None:
            self.bonus_image = cv2.resize(self.bonus_image, (50, 50),
                                          interpolation=cv2.INTER_AREA)
        else:
            print("Erreur : Impossible de charger l'image star.png.")

        self.malus_image = cv2.imread("assets/bomb.png", cv2.IMREAD_UNCHANGED)
        if self.malus_image is not None:
            self.malus_image = cv2.resize(self.malus_image, (50, 50),
                                          interpolation=cv2.INTER_AREA)
        else:
            print("Erreur : Impossible de charger l'image bomb.png.")

        # Liste contenant tous les items (bonus/malus) actifs sur le terrain
        self.items = []
        # Nombre max d'items simultanés
        self.max_items = 5

        # Rayon de la zone de collision
        self.hitbox_radius = 40

    def spawn_item(self):
        """
        Génère un bonus ou un malus aléatoirement si on n'a pas déjà atteint
        le nombre maximum (5) d'items sur le terrain.
        """
        if len(self.items) >= self.max_items:
            return  # On ne génère pas s'il y a déjà 5 items

        # Choix aléatoire entre bonus et malus
        item_type = random.choice(["bonus", "malus"])
        x = random.randint(50, self.width - 50)
        y = random.randint(50, self.height - 50)

        self.items.append({
            "type": item_type,
            "x": x,
            "y": y
        })

        print(f"Nouvel item généré : {item_type} à ({x}, {y})")

    def check_collision(self, ball, left_paddle, right_paddle):
        """
        Vérifie pour chaque item si la balle entre en collision avec lui.
        Applique l'effet correspondant et retire l'item touché.
        """
        ball_x, ball_y = ball.position

        # On parcourt la liste des items de la fin vers le début
        # pour pouvoir supprimer sans problème d'index.
        for i in reversed(range(len(self.items))):
            item = self.items[i]
            dist = np.sqrt((ball_x - item["x"])**2 + (ball_y - item["y"])**2)
            if dist <= self.hitbox_radius:
                # Collision détectée
                item_type = item["type"]
                print(f"Collision avec un {item_type} à ({item['x']}, {item['y']})")

                if item_type == "bonus":
                    # On agrandit de 30%
                    if ball.velocity[0] > 0:
                        right_paddle.height = int(right_paddle.height * 1.3)
                    else:
                        left_paddle.height = int(left_paddle.height * 1.3)
                    print("Bonus activé : raquette agrandie de 30%.")
                else:
                    # Malus : on réduit de 50%
                    if ball.velocity[0] > 0:
                        right_paddle.height = max(10, int(right_paddle.height * 0.5))
                    else:
                        left_paddle.height = max(10, int(left_paddle.height * 0.5))
                    print("Malus activé : raquette réduite de 50%.")

                # On retire l'item de la liste
                self.items.pop(i)

    def draw_transparent_image(self, frame, image, x, y):
        """
        Dessine une image (avec canal alpha) en transparence sur la frame.
        """
        if image is None:
            return

        h, w, _ = image.shape
        # Vérifie si on ne dépasse pas du cadre
        if y + h > frame.shape[0] or x + w > frame.shape[1]:
            return

        overlay = frame[y:y + h, x:x + w]
        alpha_mask = image[:, :, 3] / 255.0  # canal alpha

        for c in range(0, 3):
            overlay[:, :, c] = (
                (1.0 - alpha_mask) * overlay[:, :, c] +
                alpha_mask * image[:, :, c]
            )

        frame[y:y + h, x:x + w] = overlay

    def draw(self, frame):
        """
        Dessine tous les bonus/malus actifs sur le terrain.
        """
        for item in self.items:
            x, y = item["x"], item["y"]
            if item["type"] == "bonus":
                # Dessin de l'image star (ou cercle si image manquante)
                if self.bonus_image is not None:
                    # Centrer l'image sur l'item
                    self.draw_transparent_image(frame, self.bonus_image,
                                                x - self.bonus_image.shape[1] // 2,
                                                y - self.bonus_image.shape[0] // 2)
                else:
                    cv2.circle(frame, (x, y), 20, (0, 255, 0), -1)
            else:
                # Dessin de l'image bomb (ou cercle si image manquante)
                if self.malus_image is not None:
                    self.draw_transparent_image(frame, self.malus_image,
                                                x - self.malus_image.shape[1] // 2,
                                                y - self.malus_image.shape[0] // 2)
                else:
                    cv2.circle(frame, (x, y), 20, (0, 0, 255), -1)

            # Dessin de la hitbox pour debug (optionnel)
            # cv2.circle(frame, (x, y), self.hitbox_radius, (255, 255, 255), 1)
