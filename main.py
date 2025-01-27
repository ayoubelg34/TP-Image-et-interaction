import cv2
from PongGame import PongGame

def main():
    width, height = 800, 600
    game = PongGame(width, height)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur : impossible d'ouvrir la caméra.")
        return

    print("Début du jeu Pong. Appuyez sur 'q' pour quitter.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur : échec de la capture d'image.")
            break

        # On retourne l'image horizontalement
        frame = cv2.flip(frame, 1)
        # On redimensionne à la taille de la zone de jeu
        frame = cv2.resize(frame, (width, height))

        # On récupère la position des mains
        hand_positions = game.hand_tracker.get_hand_positions(frame, height)

        # Mise à jour de la logique du jeu
        game.update(hand_positions)

        # Dessin des éléments
        game.draw(frame)
        cv2.imshow("Pong Game", frame)

        # Vérifie si on arrête le jeu soit parce qu'un joueur a 5 points, soit par 'q'
        if game.game_over:
            # Laisser le temps de voir l'écran de fin (1 seconde par exemple)
            cv2.waitKey(1000)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Fin du jeu demandée par l'utilisateur.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Jeu terminé.")

if __name__ == "__main__":
    main()
