import cv2
from PongGame import PongGame

def main():
    """
    Point d'entrée principal du jeu Pong utilisant Mediapipe pour le suivi des mains
    et OpenCV pour l'affichage graphique.
    """
    print("Initialisation du jeu Pong.")

    # Initialisation de la caméra
    print("Tentative d'ouverture de la caméra...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur : impossible d'ouvrir la caméra.")
        return
    print("Caméra initialisée avec succès.")

    # Initialisation de la classe PongGame
    print("Initialisation de PongGame...")
    game = PongGame(640, 480)  # Largeur : 640 px, Hauteur : 480 px
    print("PongGame initialisé avec succès.")

    print("Début de la boucle du jeu.")

    while True:
        # Capture d'image depuis la caméra
        ret, frame = cap.read()
        if not ret:
            print("Erreur : échec de la capture d'image.")
            break

        # Miroir horizontal pour une interaction plus intuitive
        frame = cv2.flip(frame, 1)

        # Récupérer les positions des mains via HandTracker
        hand_positions = game.hand_tracker.get_hand_positions(frame, game.height)
        print(f"Positions des mains détectées : {hand_positions}")

        # Mettre à jour l'état du jeu
        game.update(hand_positions)

        # Dessiner les éléments du jeu (balle, raquettes, score)
        game.draw(frame)

        # Afficher le jeu
        cv2.imshow("Pong Game", frame)

        # Quitter le jeu si la touche 'q' est pressée
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Fin du jeu demandée par l'utilisateur.")
            break

    # Libérer les ressources (caméra et fenêtres)
    print("Libération des ressources...")
    cap.release()
    cv2.destroyAllWindows()
    print("Programme terminé.")

if __name__ == "__main__":
    main()
