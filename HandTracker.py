import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self):
        """
        Initialise le tracker de mains en utilisant la bibliothèque Mediapipe.
        """
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,      # Mode dynamique (suivi sur vidéo).
            max_num_hands=2,             # Nombre maximal de mains détectées.
            min_detection_confidence=0.7, # Confiance min pour la détection.
            min_tracking_confidence=0.7   # Confiance min pour le suivi.
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def get_hand_positions(self, frame, screen_height):
        """
        Récupère les positions des doigts (index) des mains dans l'image.
        :param frame: Image capturée par la caméra (BGR).
        :param screen_height: Hauteur de l'écran pour convertir la position relative en pixels.
        :return: Dictionnaire avec les positions verticales des mains détectées ("Left" et "Right").
        """
        # Convertir BGR -> RGB pour Mediapipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(frame_rgb)

        hand_positions = {"Left": None, "Right": None}

        # Vérifier si des mains sont détectées
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                # Label "Left" ou "Right"
                label = handedness.classification[0].label

                # Position verticale (relative) du bout de l'index
                index_tip_y = hand_landmarks.landmark[
                    mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP
                ].y

                # Conversion en pixels
                hand_positions[label] = int(index_tip_y * screen_height)

        return hand_positions

    def draw_hands(self, frame, results):
        """
        Dessine les points clés et connexions des mains sur l'image (optionnel).
        """
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS
                )
