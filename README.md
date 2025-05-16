# HuntDuck
# 🦆 Cazadores de Rostros – ¡Apunta con tu rostro!

**Cazadores de Rostros** es un juego estilo *Duck Hunt* hecho con **Python**, **MediaPipe** y **Pygame**, en el que **usas tu rostro frente a la cámara para apuntar y disparar**.

---

## 🎮 ¿De qué se trata?

Este juego es una reinvención moderna del clásico *Duck Hunt*, donde en lugar de usar un mouse o un control, **usas tu rostro como puntero detectado por la cámara** para interactuar con el juego.

🧏‍♂️ **Mueves tu rostro** → el cursor se mueve en la pantalla  
🦆 **Si el Pato colisiona con el puntero** → ¡disparas!

---

## 🧠 Tecnologías utilizadas

- **Python** – Lógica general del juego
- **MediaPipe** – Detección de rostro en tiempo real usando visión por computadora
- **Pygame** – Motor gráfico 2D para construir el juego

---

## 🚀 ¿Cómo funciona?

1. **MediaPipe** capta los movimientos de tu rostro a través de la cámara web.
2. Detecta la posición de tu rostro enfocandose en el ojo izquierdo.
3. Esa información se usa para:
   - **Mover el puntero**
4. **Pygame** renderiza el juego, detecta colisiones y muestra los elementos en pantalla (patos, fondo, efectos).

---

## 🛠️ Requisitos

- Python 3.7 o superior
- OpenCV (`opencv-python`)
- MediaPipe
- Pygame

## ▶️ Cómo jugar

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

Ejecuta

```bash
python main.py
```
