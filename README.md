# Impossible Snake v1.0

## Descripción

**Impossible Snake** es una versión mejorada y más desafiante del clásico juego Snake, desarrollada con Pygame. Incluye múltiples niveles de dificultad, una variedad de power-ups y power-downs, obstáculos, efectos visuales como niebla, y un sistema persistente de puntuación máxima.

**Desarrollado** por [RafaelSanguinoAriza].

## Características

* **Jugabilidad Clásica de Snake:** Controla una serpiente que crece al comer comida, evitando chocar contra los bordes, obstáculos y su propio cuerpo.
* **Múltiples Niveles de Dificultad:**
    * **Fácil:** Velocidad inicial baja, sin obstáculos.
    * **Normal:** Velocidad moderada, pocos obstáculos, mezcla de power-ups y power-downs.
    * **Difícil:** Velocidad alta, más obstáculos, mezcla de power-ups y power-downs.
    * **Imposible:** Velocidad muy alta, muchos obstáculos, controles **invertidos permanentemente**, efecto de **niebla** periódica, y **solo aparecen power-downs**.
* **Power-ups (Beneficiosos):**
    * `Bonus`: Otorga puntos extra.
    * `Invincibility`: Te hace temporalmente invulnerable a colisiones (excepto la comida mortal). Permite atravesar bordes.
    * `Speed Up`: Aumenta la velocidad.
    * `Shrink`: Reduce el tamaño de la serpiente.
    * `Multiplier`: Duplica los puntos obtenidos por comida normal temporalmente.
* **Power-downs (Perjudiciales):**
    * `Poison`: Resta puntos.
    * `Death`: Causa Game Over instantáneo.
    * `Slow Down`: Reduce la velocidad de la serpiente.
    * `Reverse`: Invierte los controles de dirección temporalmente (en modos Normal/Difícil).
* **Obstáculos:** Bloques estáticos que causan Game Over si la serpiente choca contra ellos (en modos Normal, Difícil e Imposible).
* **Efecto de Niebla (Modo Imposible):** Un efecto visual que oscurece periódicamente la pantalla, dejando solo un círculo de visión alrededor de la cabeza de la serpiente.
* **Puntuación Máxima Persistente:** Guarda y carga la puntuación más alta lograda en un archivo (`snake_highscore.txt`).
* **Sonidos:** Efectos de sonido generados dinámicamente para comer, game over, aparición y recolección de power-ups/downs (requiere `numpy`).
* **Interfaz Gráfica:** Pantallas de título, selección de dificultad, pausa y Game Over. Panel de puntuación en tiempo real con indicadores.
* **Icono de Ventana:** Intenta cargar un archivo `Snake.png` como icono de la ventana del juego.

## Requisitos

* **Python 3.x**
* **Pygame:** Biblioteca para desarrollo de juegos.
    ```bash
    pip install pygame
    ```
* **NumPy:** Biblioteca para cálculo numérico (usada aquí para generar sonidos).
    ```bash
    pip install numpy
    ```

## Cómo Jugar

1.  **Instala los requisitos:** Asegúrate de tener Python, Pygame y NumPy instalados.
2.  **(Opcional):** Coloca un archivo de imagen llamado `Snake.png` en el mismo directorio que el script para que se use como icono de la ventana.
3.  **Ejecuta el script:** Abre una terminal o línea de comandos, navega hasta el directorio donde guardaste el archivo `.py` y ejecuta:
    ```bash
    python Impossible_Snake_v1.0.py.py
    ```
4.  **Pantalla de Título:** Presiona cualquier tecla para continuar.
5.  **Selección de Dificultad:** Presiona las teclas numéricas `1`, `2`, `3` o `4` para elegir la dificultad (Fácil, Normal, Difícil, Imposible).
6.  **Juego:**
    * Usa las **Teclas de Flecha** o las teclas **WASD** para controlar la dirección de la serpiente.
    * **Recuerda:** En modo Imposible los controles estarán invertidos.
    * Come la comida roja (`FOOD_NORMAL_COLOR`) para crecer y aumentar tu puntuación y velocidad.
    * Interactúa con los power-ups/downs (círculos de colores) que aparecen. ¡Ten cuidado con los perjudiciales!
    * Evita chocar contra los bordes de la pantalla (excepto si eres invencible), los obstáculos grises (`OBSTACLE_COLOR`), y tu propio cuerpo.
7.  **Pausa:** Presiona la tecla `P` para pausar o reanudar el juego.
8.  **Game Over:** Si chocas, aparecerá la pantalla de Game Over.
    * Presiona `R` para reintentar en la misma dificultad.
    * Presiona `Q` para volver a la pantalla de selección de dificultad.
9.  **Salir:** Presiona la tecla `ESC` en cualquier momento (excepto en la pantalla de Game Over, donde es `Q`) o cierra la ventana para salir del juego.

## Archivos

* `nombre_del_script.py`: El código fuente principal del juego.
* `snake_highscore.txt`: Archivo de texto creado automáticamente para guardar la puntuación máxima.
* `Snake.png` (Opcional): Icono para la ventana del juego.

## Contribuye al Proyecto

¡Tu ayuda es bienvenida! Si tienes ideas para mejorar este proyecto, encuentra un error o deseas agregar nuevas funcionalidades, no dudes en contribuir.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.


¡Disfruta del desafío!




