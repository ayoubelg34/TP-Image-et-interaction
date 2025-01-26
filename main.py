import cv2
import mediapipe as mp
import numpy as np
from PongGame import PongGame

def main():
    """
    Point d'entrée principal du jeu Pong utilisant Mediapipe pour le suivi des mains
    et OpenCV pour l'affichage graphique.
    """
    # Ouvrir la caméra (index 0 correspond à la caméra par défaut).
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur d'ouverture de la caméra.")
        return  # Quitter si la caméra n'est pas accessible.
    if cap.isOpened():
        print("Caméra initialisée avec succès.")

    # Initialisation du jeu Pong avec une résolution définie.
    game = PongGame(640, 480)  # Largeur: 640 pixels, Hauteur: 480 pixels.

    while True:
        # Lire une image depuis la caméra.
        ret, frame = cap.read()
        if not ret:
            break  # Quitter la boucle si la lecture échoue.

        # Miroir horizontal pour un affichage plus naturel (comme un miroir).
        frame = cv2.flip(frame, 1)

        # Redimensionner l'image pour correspondre à la taille du jeu.
        frame = cv2.resize(frame, (640, 480))

        # Récupérer les positions des mains à partir de l'image capturée.
        hand_positions = game.hand_tracker.get_hand_positions(frame, game.height)

        # Mettre à jour l'état du jeu en fonction des positions des mains.
        game.update(hand_positions)

        # Dessiner les éléments du jeu (balle, raquettes, etc.) sur le cadre.
        game.draw(frame)

        # Afficher l'image mise à jour avec les éléments du jeu.
        cv2.imshow("Pong Game", frame)

        # Quitter le jeu si la touche "q" est pressée.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libérer les ressources (caméra et fenêtres).
    cap.release()
    cv2.destroyAllWindows()

# Vérifier si le script est exécuté directement.
if __name__ == "__main__":
    main()