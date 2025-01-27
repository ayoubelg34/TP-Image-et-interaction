import cv2
from PongGame import PongGame

def main():
    # Dimensions de la fenêtre du jeu
    width, height = 800, 600

    # Initialisation du jeu
    game = PongGame(width, height)

    # Initialisation de la capture vidéo
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur : impossible d'ouvrir la caméra.")
        return

    print("Début du jeu Pong. Appuyez sur 'q' pour quitter.")

    while True:
        # Lecture de la frame
        ret, frame = cap.read()
        if not ret:
            print("Erreur : échec de la capture d'image.")
            break

        # Retourner l'image horizontalement
        frame = cv2.flip(frame, 1)

        # Redimensionner l'image à la taille du jeu
        frame = cv2.resize(frame, (width, height))

        # Récupérer les positions des mains
        hand_positions = game.hand_tracker.get_hand_positions(frame, height)

        # Mettre à jour l'état du jeu
        game.update(hand_positions)

        # Dessiner le jeu
        game.draw(frame)

        # Afficher la fenêtre
        cv2.imshow("Pong Game", frame)

        # Vérifier si l'on doit quitter
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Fin du jeu demandée par l'utilisateur.")
            break

        # Si le jeu est fini (un des joueurs a 5 points), on quitte la boucle
        if game.game_over:
            # Laisser le temps de voir l'écran de fin
            cv2.waitKey(2000)
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Jeu terminé.")

if __name__ == "__main__":
    main()
