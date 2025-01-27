import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self):
        """
        Initialise le tracker de mains en utilisant la bibliothèque Mediapipe.
        """
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def get_hand_positions(self, frame, screen_height):
        """
        Récupère les positions (en y) du bout de l'index pour chaque main.
        Retourne un dict: {"Left": y_gauche, "Right": y_droite} en pixels.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(frame_rgb)

        hand_positions = {"Left": None, "Right": None}

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                label = handedness.classification[0].label  # "Left" ou "Right"
                index_tip_y = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y
                # Conversion en pixels
                hand_positions[label] = int(index_tip_y * screen_height)

        return hand_positions

    def draw_hands(self, frame, results):
        """
        Dessine la détection des mains (optionnel).
        """
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS
                )
