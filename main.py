import cv2
from PongGame import PongGame

def main():
    # Dimensions du jeu
    width, height = 800, 600

    # Initialisation du jeu
    game = PongGame(width, height)

    # Initialisation de la capture vidéo
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur : impossible d'ouvrir la caméra.")
        return

    print("Début du jeu Pong. Appuyez sur 'q' pour quitter.")

    # Boucle principale du jeu
    while True:
        try:
            # Capture d'image
            ret, frame = cap.read()
            if not ret:
                print("Erreur : échec de la capture d'image.")
                break

            # Retourner l'image horizontalement pour corriger l'inversion
            frame = cv2.flip(frame, 1)

            # Redimensionner l'image pour qu'elle corresponde à la taille du jeu
            frame = cv2.resize(frame, (width, height))

            # Récupération des positions des mains
            hand_positions = game.hand_tracker.get_hand_positions(frame, game.height)
            print(f"Positions des mains détectées : {hand_positions}")

            # Mettre à jour l'état du jeu
            print("Mise à jour du jeu...")
            game.update(hand_positions)

            # Dessiner les éléments du jeu
            print("Dessin du jeu...")
            game.draw(frame)

            # Afficher la fenêtre de jeu
            cv2.imshow("Pong Game", frame)

            # Quitter si 'q' est pressé
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Fin du jeu demandée par l'utilisateur.")
                break

        except Exception as e:
            print(f"Erreur inattendue : {e}")
            break

    # Libérer les ressources
    cap.release()
    cv2.destroyAllWindows()
    print("Jeu terminé.")

if __name__ == "__main__":
    main()
