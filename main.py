import cv2
from PongGame import PongGame
import sys
import os
import pygame

def menu(screen, clock):
    """
    Affiche un menu avec une image de fond et un bouton pour démarrer le jeu.
    """
    # Charger l'image de fond
    try:
        background = pygame.image.load("assets/fond.png")  
        background = pygame.transform.scale(background, (800, 600))  # Adapter à la fenêtre
    except pygame.error as e:
        print(f"Erreur : Impossible de charger l'image de fond : {e}")
        return False

    # Définir la police
    font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 36)

    # Boucle du menu
    while True:
        screen.blit(background, (0, 0))  # Dessiner l'image de fond

        # Afficher le titre
        title_text = font.render("Pong Amélioré", True, (255, 255, 255))
        screen.blit(title_text, (250, 100))

        # Dessiner le bouton
        button_rect = pygame.Rect(300, 300, 200, 60)  # Position et taille du bouton
        pygame.draw.rect(screen, (0, 128, 255), button_rect)
        pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)  # Bordure

        # Texte sur le bouton
        button_text = button_font.render("Démarrer", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Quitter le programme
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    return True  # Lancer le jeu si le bouton est cliqué

        pygame.display.flip()
        clock.tick(60)

def main():
    # Initialiser pygame
    pygame.init()
    pygame.mixer.init()

    # Configuration de la fenêtre
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong Amélioré")
    clock = pygame.time.Clock()

    # Afficher le menu avant de lancer le jeu
    if not menu(screen, clock):
        pygame.quit()
        sys.exit()

    try:
        pygame.mixer.music.load("assets/freedom.mp3")  
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Erreur lors du chargement de la musique : {e}")

    # Lancer le jeu
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

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (width, height))

        hand_positions = game.hand_tracker.get_hand_positions(frame, height)
        game.update(hand_positions)
        game.draw(frame)

        cv2.imshow("Pong Game", frame)

        if game.game_over:
            cv2.waitKey(1000)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Fin du jeu demandée par l'utilisateur.")
            break

    pygame.mixer.music.stop()
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    print("Jeu terminé.")

if __name__ == "__main__":
    main()
