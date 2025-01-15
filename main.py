import cv2
import mediapipe as mp
import numpy as np

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur d'ouverture de la caméra.")
        return

    game = PongGame(640, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))

        hand_positions = game.hand_tracker.get_hand_positions(frame, game.height)
        game.update(hand_positions)
        game.draw(frame)

        cv2.imshow("Pong Game", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
