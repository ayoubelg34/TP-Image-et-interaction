import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self):
        """
        Initialise le tracker de mains en utilisant la bibliothèque Mediapipe.
        """
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,      # Mode dynamique
            max_num_hands=2,             # Nombre maximal de mains
            min_detection_confidence=0.7, # Confiance min pour la détection
            min_tracking_confidence=0.7   # Confiance min pour le suivi
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def get_hand_positions(self, frame, screen_height):
        """
        Récupère les positions (y) de l'index des mains dans l'image.
        :param frame: Image capturée (BGR).
        :param screen_height: Hauteur en pixels pour convertir la position relative.
        :return: dict { "Left": y_pixels, "Right": y_pixels }
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(frame_rgb)

        hand_positions = {"Left": None, "Right": None}

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                label = handedness.classification[0].label
                index_tip_y = hand_landmarks.landmark[
                    mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP
                ].y
                # Conversion en pixels
                hand_positions[label] = int(index_tip_y * screen_height)

        return hand_positions

    def draw_hands(self, frame, results):
        """
        Dessine les points clés des mains (optionnel).
        """
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS
                )
