# mano.py
import cv2
import mediapipe as mp
from math import sqrt

class DetectorMano:
    def __init__(self, ancho, alto):
        self.cap = cv2.VideoCapture(0)
        self.ancho = ancho
        self.alto = alto
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.resultado = None
        self.cursor = (0, 0)
        self.disparo = False

    def distancia(self, p1, p2):
        return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def actualizar(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.resultado = self.hands.process(rgb)

        self.disparo = False
        if self.resultado.multi_hand_landmarks:
            hand = self.resultado.multi_hand_landmarks[0]
            puntos = hand.landmark
            dedo_indice = puntos[8]
            pulgar = puntos[4]

            # Posición del cursor escalada al tamaño del juego
            x = int(dedo_indice.x * self.ancho)
            y = int(dedo_indice.y * self.alto)
            self.cursor = (x, y)

            # Disparo si pulgar y índice están cerca
            if self.distancia(dedo_indice, pulgar) < 0.05:
                self.disparo = True

    def cerrar(self):
        self.cap.release()
        cv2.destroyAllWindows()
