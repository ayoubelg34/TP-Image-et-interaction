import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    def __init__(self):
        """
        Initialise le tracker de mains en utilisant la bibliothèque Mediapipe.
        """
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,  # Mode dynamique (détection continue sur des vidéos).
            max_num_hands=2,  # Nombre maximal de mains détectées simultanément.
            min_detection_confidence=0.7,  # Confiance minimale pour considérer une détection comme valide.
            min_tracking_confidence=0.7  # Confiance minimale pour le suivi des points clés des mains.
        )
        self.mp_drawing = mp.solutions.drawing_utils  # Outil pour dessiner les points et les connexions.

    def get_hand_positions(self, frame, screen_height):
        """
        Récupère les positions des doigts des mains dans l'image.

        :param frame: Image capturée par la caméra (matrice numpy en format BGR).
        :param screen_height: Hauteur de l'écran en pixels pour convertir les positions relatives en absolues.
        :return: Un dictionnaire contenant les positions verticales des index des mains détectées ("Left" et "Right").
        """
        # Convertir l'image de BGR (OpenCV) à RGB (Mediapipe attend un format RGB).
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Traiter l'image pour détecter les mains et leurs points clés.
        results = self.mp_hands.process(frame_rgb)

        # Initialiser un dictionnaire pour stocker les positions des mains ("Left" et "Right").
        hand_positions = {"Left": None, "Right": None}

        # Vérifier si des mains sont détectées et si leur classification (droite/gauche) est disponible.
        if results.multi_hand_landmarks and results.multi_handedness:
            # Parcourir les points clés des mains et leur classification respective.
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Obtenir le label "Left" ou "Right".
                label = handedness.classification[0].label

                # Récupérer la position verticale (relative) du bout de l'index.
                index_tip_y = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y

                # Convertir la position relative (0 à 1) en pixels (valeur absolue).
                hand_positions[label] = int(index_tip_y * screen_height)

        # Retourner le dictionnaire avec les positions des mains.
        return hand_positions

    def draw_hands(self, frame, results):
        """
        Dessine les points clés et les connexions des mains sur l'image.

        :param frame: Image sur laquelle dessiner les mains (matrice numpy).
        :param results: Résultats de détection des mains retournés par Mediapipe.
        """
        # Vérifier si des mains sont détectées.
        if results.multi_hand_landmarks:
            # Dessiner les points clés et les connexions pour chaque main détectée.
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,  # Image sur laquelle dessiner.
                    hand_landmarks,  # Points clés des mains.
                    mp.solutions.hands.HAND_CONNECTIONS  # Connexions entre les points (ex. doigts).
                )

