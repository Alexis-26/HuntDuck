import cv2
import mediapipe as mp
from math import sqrt
import time
# forma de pistola
# class DetectorMano:
#     def __init__(self, ancho, alto):
#         self.cap = cv2.VideoCapture(0)
#         self.ancho = ancho
#         self.alto = alto
#         self.mp_hands = mp.solutions.hands
#         self.hands = self.mp_hands.Hands(
#             max_num_hands=1,
#             min_detection_confidence=0.7,
#             min_tracking_confidence=0.7
#         )
#         self.resultado = None
#         self.cursor = (0, 0)
#         self.disparo = False
#         self.ultimo_disparo = 0
#         self.cooldown = 0.5  # segundos entre disparos

#     def distancia(self, p1, p2):
#         return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

#     def actualizar(self):
#         ret, frame = self.cap.read()
#         if not ret:
#             return

#         frame = cv2.flip(frame, 1)  # Voltea la imagen horizontalmente
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         self.resultado = self.hands.process(rgb)

#         self.disparo = False
#         if self.resultado.multi_hand_landmarks:
#             hand = self.resultado.multi_hand_landmarks[0]
#             puntos = hand.landmark

#             # Calcular el centro de la palma
#             x_total = 0
#             y_total = 0
#             puntos_palm = [puntos[i] for i in range(5)]  # Puntos de la palma (0, 1, 2, 3, 4)

#             # Sumar las posiciones X e Y de estos puntos
#             for p in puntos_palm:
#                 x_total += p.x
#                 y_total += p.y

#             # Calcular el centro de la palma
#             x_centro = int((x_total / len(puntos_palm)) * self.ancho)
#             y_centro = int((y_total / len(puntos_palm)) * self.alto)
#             self.cursor = (x_centro, y_centro)

#             # Visualización: dibuja un círculo en el centro de la palma
#             cv2.circle(frame, (x_centro, y_centro), 15, (0, 255, 255), -1)

#             # Ahora, se podría hacer el disparo con la misma lógica, como cuando el índice y el pulgar se tocan.
#             # Puedes mantener el mismo control de disparo, pero ahora usando la mano completa como puntero.

#             # Puntos de la yema del pulgar y del índice para verificar la acción de disparo
#             yema_indice = puntos[8]
#             yema_pulgar = puntos[4]
#             distancia = self.distancia(yema_indice, yema_pulgar)

#             # Detectar si el índice está estirado (más arriba que el nudillo)
#             nudillo_indice = puntos[6]
#             dedo_estirado = yema_indice.y < nudillo_indice.y  # más arriba en pantalla

#             # Disparo si toca con el pulgar y está estirado el índice
#             ahora = time.time()
#             if distancia < 0.08 and dedo_estirado and (ahora - self.ultimo_disparo > self.cooldown):
#                 self.disparo = True
#                 self.ultimo_disparo = ahora
#                 cv2.putText(frame, "¡DISPARO!", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

#         # Mostrar la cámara con anotaciones
#         cv2.imshow("Mano Detector", frame)
#         cv2.waitKey(1)

#     def cerrar(self):
#         self.cap.release()
#         cv2.destroyAllWindows()


 # Dos manos
# import cv2
# import mediapipe as mp
# from math import sqrt
# import time

# class DetectorMano:
#     def __init__(self, ancho, alto):
#         self.cap = cv2.VideoCapture(0)
#         self.ancho = ancho
#         self.alto = alto
#         self.mp_hands = mp.solutions.hands
#         self.hands = self.mp_hands.Hands(
#             max_num_hands=2,
#             min_detection_confidence=0.7,
#             min_tracking_confidence=0.7
#         )
#         self.resultado = None
#         self.cursor = (0, 0)
#         self.disparo = False
#         self.ultimo_disparo = 0
#         self.cooldown = 0.5

#     def distancia(self, p1, p2):
#         return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

#     def actualizar(self):
#         ret, frame = self.cap.read()
#         if not ret:
#             return

#         frame = cv2.flip(frame, 1)
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         self.resultado = self.hands.process(rgb)

#         self.disparo = False
#         mano_derecha = None
#         mano_izquierda = None

#         if self.resultado.multi_hand_landmarks and self.resultado.multi_handedness:
#             for i, mano in enumerate(self.resultado.multi_hand_landmarks):
#                 tipo_mano = self.resultado.multi_handedness[i].classification[0].label

#                 if tipo_mano == 'Right':
#                     mano_derecha = mano
#                 elif tipo_mano == 'Left':
#                     mano_izquierda = mano

#             # Usar la mano derecha como puntero
#             if mano_derecha:
#                 puntos = mano_derecha.landmark
#                 x_total = 0
#                 y_total = 0
#                 puntos_palm = [puntos[i] for i in range(5)]
#                 for p in puntos_palm:
#                     x_total += p.x
#                     y_total += p.y
#                 x_centro = int((x_total / len(puntos_palm)) * self.ancho)
#                 y_centro = int((y_total / len(puntos_palm)) * self.alto)
#                 self.cursor = (x_centro, y_centro)
#                 cv2.circle(frame, self.cursor, 15, (0, 255, 255), -1)

#             # Usar la mano izquierda para disparar
#             if mano_izquierda:
#                 puntos = mano_izquierda.landmark
#                 yema_indice = puntos[8]
#                 yema_pulgar = puntos[4]
#                 distancia_dedos = self.distancia(yema_indice, yema_pulgar)
#                 ahora = time.time()
#                 if distancia_dedos < 0.08 and (ahora - self.ultimo_disparo > self.cooldown):
#                     self.disparo = True
#                     self.ultimo_disparo = ahora
#                     cv2.putText(frame, "¡DISPARO!", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

#         cv2.imshow("Detector Dos Manos", frame)
#         cv2.waitKey(1)

#     def cerrar(self):
#         self.cap.release()
#         cv2.destroyAllWindows()


# Ojos y mano
# class DetectorMano:
#     def __init__(self, ancho, alto):
#         self.cap = cv2.VideoCapture(0)
#         self.ancho = ancho
#         self.alto = alto
#         self.mp_hands = mp.solutions.hands
#         self.hands = self.mp_hands.Hands(
#             max_num_hands=1,
#             min_detection_confidence=0.7,
#             min_tracking_confidence=0.7
#         )
#         self.mp_face_mesh = mp.solutions.face_mesh
#         self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False)
        
#         self.resultado_hands = None
#         self.resultado_face = None
#         self.cursor = (0, 0)
#         self.disparo = False
#         self.ultimo_disparo = 0
#         self.cooldown = 0.5  # segundos entre disparos

#     def distancia(self, p1, p2):
#         return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

#     def actualizar(self):
#         ret, frame = self.cap.read()
#         if not ret:
#             return

#         frame = cv2.flip(frame, 1)  # Voltea la imagen horizontalmente
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
#         # Procesar la mano para el disparo
#         self.resultado_hands = self.hands.process(rgb)
        
#         # Procesar la cara para el puntero con la mirada
#         self.resultado_face = self.face_mesh.process(rgb)

#         # Inicializar disparo en False
#         self.disparo = False
        
#         # Detectar el puntero con la mirada
#         if self.resultado_face.multi_face_landmarks:
#             for rostro in self.resultado_face.multi_face_landmarks:
#                 # Ojo derecho (vista del usuario, lado izquierdo del frame)
#                 ojo_derecho = [33, 133]  # esquina interna y externa
#                 x_ojo = int((rostro.landmark[ojo_derecho[0]].x + rostro.landmark[ojo_derecho[1]].x) / 2 * self.ancho)
#                 y_ojo = int((rostro.landmark[ojo_derecho[0]].y + rostro.landmark[ojo_derecho[1]].y) / 2 * self.alto)

#                 # Actualizar el puntero con la pupila
#                 self.cursor = (x_ojo, y_ojo)
                
#                 # Dibujar la posición estimada de la pupila
#                 cv2.circle(frame, (x_ojo, y_ojo), 8, (255, 0, 0), -1)
#                 cv2.circle(frame, (x_ojo, y_ojo), 15, (0, 255, 255), 2)
        
#         # Detectar el disparo con la mano
#         if self.resultado_hands.multi_hand_landmarks:
#             hand = self.resultado_hands.multi_hand_landmarks[0]
#             puntos = hand.landmark

#             # Calcular el centro de la palma
#             x_total = 0
#             y_total = 0
#             puntos_palm = [puntos[i] for i in range(5)]  # Puntos de la palma (0, 1, 2, 3, 4)

#             # Sumar las posiciones X e Y de estos puntos
#             for p in puntos_palm:
#                 x_total += p.x
#                 y_total += p.y

#             # Calcular el centro de la palma
#             x_centro = int((x_total / len(puntos_palm)) * self.ancho)
#             y_centro = int((y_total / len(puntos_palm)) * self.alto)

#             # Visualización: dibuja un círculo en el centro de la palma
#             cv2.circle(frame, (x_centro, y_centro), 15, (0, 255, 255), -1)

#             # Puntos de la yema del pulgar y del índice para verificar la acción de disparo
#             yema_indice = puntos[8]
#             yema_pulgar = puntos[4]
#             distancia = self.distancia(yema_indice, yema_pulgar)

#             # Detectar si el índice está estirado (más arriba que el nudillo)
#             nudillo_indice = puntos[6]
#             dedo_estirado = yema_indice.y < nudillo_indice.y  # más arriba en pantalla

#             # Disparo si toca con el pulgar y está estirado el índice
#             ahora = time.time()
#             if distancia < 0.08 and dedo_estirado and (ahora - self.ultimo_disparo > self.cooldown):
#                 self.disparo = True
#                 self.ultimo_disparo = ahora
#                 cv2.putText(frame, "¡DISPARO!", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

#         # Mostrar la cámara con anotaciones
#         cv2.imshow("Mano y Vista Detector", frame)
#         cv2.waitKey(1)

#     def cerrar(self):
#         self.cap.release()
#         cv2.destroyAllWindows()

# version 2
# class DetectorMano:
#     def __init__(self, ancho, alto):
#         self.ancho = ancho
#         self.alto = alto

#         # Captura de cámara
#         self.cap = cv2.VideoCapture(0)
#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.ancho)
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.alto)

#         # Obtener dimensiones reales del frame
#         self.frame_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#         self.frame_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

#         # Mediapipe
#         self.mp_hands = mp.solutions.hands
#         self.hands = self.mp_hands.Hands(
#             max_num_hands=1,
#             min_detection_confidence=0.7,
#             min_tracking_confidence=0.7
#         )
#         self.mp_face_mesh = mp.solutions.face_mesh
#         self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False)

#         self.resultado_hands = None
#         self.resultado_face = None
#         self.cursor = (0, 0)
#         self.disparo = False
#         self.ultimo_disparo = 0
#         self.cooldown = 0.5  # segundos entre disparos

#     def distancia(self, p1, p2):
#         return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

#     def actualizar(self):
#         ret, frame = self.cap.read()
#         if not ret:
#             return

#         frame = cv2.flip(frame, 1)
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         self.resultado_hands = self.hands.process(rgb)
#         self.resultado_face = self.face_mesh.process(rgb)
#         self.disparo = False

#         if self.resultado_face.multi_face_landmarks:
#             for rostro in self.resultado_face.multi_face_landmarks:
#                 ojo_derecho = [33, 133]
#                 x_ojo_frame = int((rostro.landmark[ojo_derecho[0]].x + rostro.landmark[ojo_derecho[1]].x) / 2 * self.frame_width)
#                 y_ojo_frame = int((rostro.landmark[ojo_derecho[0]].y + rostro.landmark[ojo_derecho[1]].y) / 2 * self.frame_height)

#                 # Escalar a ventana de Pygame
#                 x_ventana = int(x_ojo_frame * self.ancho / self.frame_width)
#                 y_ventana = int(y_ojo_frame * self.alto / self.frame_height)
#                 self.cursor = (x_ventana, y_ventana)

#                 cv2.circle(frame, (x_ojo_frame, y_ojo_frame), 8, (255, 0, 0), -1)
#                 cv2.circle(frame, (x_ojo_frame, y_ojo_frame), 15, (0, 255, 255), 2)

#         if self.resultado_hands.multi_hand_landmarks:
#             hand = self.resultado_hands.multi_hand_landmarks[0]
#             puntos = hand.landmark
#             puntos_palm = [puntos[i] for i in range(5)]

#             x_total = sum(p.x for p in puntos_palm)
#             y_total = sum(p.y for p in puntos_palm)
#             x_centro = int((x_total / len(puntos_palm)) * self.frame_width)
#             y_centro = int((y_total / len(puntos_palm)) * self.frame_height)

#             cv2.circle(frame, (x_centro, y_centro), 15, (0, 255, 255), -1)

#             yema_indice = puntos[8]
#             yema_pulgar = puntos[4]
#             distancia = self.distancia(yema_indice, yema_pulgar)

#             nudillo_indice = puntos[6]
#             dedo_estirado = yema_indice.y < nudillo_indice.y

#             ahora = time.time()
#             if distancia < 0.08 and dedo_estirado and (ahora - self.ultimo_disparo > self.cooldown):
#                 self.disparo = True
#                 self.ultimo_disparo = ahora
#                 cv2.putText(frame, "¡DISPARO!", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
#         # Calibración: mostrar punto guía en el centro
#         cv2.circle(frame, (int(self.frame_width // 2), int(self.frame_height // 2)), 10, (0, 255, 0), -1)
#         cv2.putText(frame, "Mira al punto verde para calibrar", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

#         #cv2.imshow("Mano y Vista Detector", frame)
#         cv2.waitKey(1)

#     def cerrar(self):
#         self.cap.release()
#         cv2.destroyAllWindows()


# class DetectorMano:
#     def __init__(self, ancho, alto):
#         self.ancho = ancho
#         self.alto = alto

#         # Captura de cámara con resolución ajustada
#         self.cap = cv2.VideoCapture(0)
#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.ancho // 2)  # Reducir resolución
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.alto // 2)

#         # Obtener dimensiones reales del frame
#         self.frame_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#         self.frame_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

#         # Mediapipe FaceMesh
#         self.mp_face_mesh = mp.solutions.face_mesh
#         self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False)

#         self.resultado_face = None
#         self.cursor = (0, 0)

#     def obtener_posicion_centro_ojos(self, rostro):
#         """
#         Calcula el centro entre los dos ojos basándose en los puntos clave detectados por MediaPipe FaceMesh.
#         """
#         ojo_izquierdo = rostro.landmark[33]  # Ojo izquierdo
#         ojo_derecho = rostro.landmark[263]   # Ojo derecho

#         # Calcular el centro entre ambos ojos
#         x_centro = int((ojo_izquierdo.x + ojo_derecho.x) / 2 * self.frame_width)
#         y_centro = int((ojo_izquierdo.y + ojo_derecho.y) / 2 * self.frame_height)
#         return x_centro, y_centro

#     def actualizar(self):
#         ret, frame = self.cap.read()
#         if not ret:
#             return

#         frame = cv2.flip(frame, 1)
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         self.resultado_face = self.face_mesh.process(rgb)

#         if self.resultado_face.multi_face_landmarks:
#             for rostro in self.resultado_face.multi_face_landmarks:
#                 # Obtener la posición del centro entre los dos ojos
#                 x_centro, y_centro = self.obtener_posicion_centro_ojos(rostro)
#                 self.cursor = (x_centro, y_centro)

#                 # Visualizar el centro entre los ojos
#                 cv2.circle(frame, (x_centro, y_centro), 8, (255, 0, 0), -1)
#                 cv2.circle(frame, (x_centro, y_centro), 15, (0, 255, 255), 2)

#         # Calibración: mostrar punto guía en el centro
#         cv2.circle(frame, (int(self.frame_width // 2), int(self.frame_height // 2)), 10, (0, 255, 0), -1)
#         cv2.putText(frame, "Mira al punto verde para calibrar", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

#         # Mostrar la imagen
#         cv2.imshow("Rostro Detector", frame)
#         cv2.waitKey(1)

#     def cerrar(self):
#         self.cap.release()
#         cv2.destroyAllWindows()

import cv2
import mediapipe as mp

class DetectorMano:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

        # Captura de cámara
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.ancho)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.alto)

        # Obtener dimensiones reales del frame
        self.frame_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Mediapipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False)

        self.resultado_face = None
        self.cursor = (0, 0)

    def actualizar(self):
        # Leer un frame de la cámara
        ret, frame = self.cap.read()
        if not ret:
            return

        # Volteamos el frame para una visualización tipo espejo
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesamos el rostro
        self.resultado_face = self.face_mesh.process(rgb)

        # Detectar rostro y mover cursor solo basado en los ojos
        if self.resultado_face.multi_face_landmarks:
            for rostro in self.resultado_face.multi_face_landmarks:
                ojo_derecho = [33, 133]
                x_ojo_frame = int((rostro.landmark[ojo_derecho[0]].x + rostro.landmark[ojo_derecho[1]].x) / 2 * self.frame_width)
                y_ojo_frame = int((rostro.landmark[ojo_derecho[0]].y + rostro.landmark[ojo_derecho[1]].y) / 2 * self.frame_height)

                # Escalar a ventana de Pygame
                x_ventana = int(x_ojo_frame * self.ancho / self.frame_width)
                y_ventana = int(y_ojo_frame * self.alto / self.frame_height)
                self.cursor = (x_ventana, y_ventana)

                # Visualizar el centro entre los ojos
                cv2.circle(frame, (x_ojo_frame, y_ojo_frame), 8, (255, 0, 0), -1)
                cv2.circle(frame, (x_ojo_frame, y_ojo_frame), 15, (0, 255, 255), 2)

        # Calibración: mostrar punto guía en el centro
        cv2.circle(frame, (int(self.frame_width // 2), int(self.frame_height // 2)), 10, (0, 255, 0), -1)
        cv2.putText(frame, "Mira al punto verde para calibrar", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Mostrar el frame con las modificaciones
        #cv2.imshow("Rostro y Vista Detector", frame)
        cv2.waitKey(1)

    def cerrar(self):
        self.cap.release()
        cv2.destroyAllWindows()
