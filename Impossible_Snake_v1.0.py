# --- Importaciones de Bibliotecas ---

import pygame  # Importar la biblioteca pygame para gráficos y manejo de eventos
import sys  # Importar sys para manejar la salida del programa
import random  # Importar random para generar posiciones aleatorias (comida, power-ups, obstáculos)
import time  # Importar time para manejar temporizadores y efectos basados en tiempo
import math  # Importar math para cálculos matemáticos (como ángulos y distancias)
import os  # Importar os interactuar con el sistema operativo (guardar/cargar highscore)
import numpy  # Importar numpy cálculos numéricos (generación de sonido)

# --- Inicialización General de Pygame y Mixer ---

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # Inicializar todos los módulos de Pygame
try:
    pygame.mixer.init()  # Inicializar el módulo de sonido
    mixer_initialized = True  # Flag para saber si el sonido está disponible
except pygame.error as e:
    print(f"Error inicializando pygame.mixer: {e}. El juego continuará sin sonido.")
    mixer_initialized = False


# --- Constantes Globales del Juego ---

# Dimensiones de la pantalla
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

# Tamaño de elementos y rejilla
BLOCK_SIZE = 15
GRID_LINE_WIDTH = 1
SCORE_PANEL_HEIGHT = 45

# Parámetros de Dificultad (Velocidad inicial)
SPEED_EASY = 7  # Velocidad para el nuevo modo facil
SPEED_NORMAL = 11  # Velocidad para el nuevo modo normal
SPEED_HARD = 18  # Velocidad para el nuevo modo difícil
SPEED_IMPOSSIBLE = 25  # Velocidad para el nuevo modo imposible
MIN_SPEED = 3  # Velocidad mínima para la serpiente

# --- Definición de Tipos de Power-ups y Power-downs ---

# Power-ups (Beneficiosos)
POWERUP_BONUS = "bonus"
POWERUP_INVINCIBILITY = "invincibility"
POWERUP_SPEEDUP = "speedup"
POWERUP_SHRINK = "shrink"
POWERUP_MULTIPLIER = "multiplier"
# Power-downs (Perjudiciales)
POWERUP_POISON = "poison"
POWERUP_DEATH = "death"
POWERUP_SLOWDOWN = "slowdown"
POWERUP_REVERSE = "reverse"

# Lista completa para spawn aleatorio (Modos Normales)
POWERUP_TYPES_NORMAL = [
    POWERUP_BONUS, # Comida bonus
    POWERUP_INVINCIBILITY, # Power-up de invencibilidad
    POWERUP_SPEEDUP, # Power-up de aumento de velocidad
    POWERUP_SHRINK, # Power-up de reducción de tamaño
    POWERUP_MULTIPLIER, # Power-up de multiplicador de puntuación
    POWERUP_POISON, # Comida venenosa
    POWERUP_DEATH, # Comida mortal
    POWERUP_SLOWDOWN, # Power-down de reducción de velocidad
    POWERUP_REVERSE, # Power-down de control invertido
]
# Lista solo con Power-Downs (Modo Imposible)
POWERUP_TYPES_IMPOSSIBLE = [
    POWERUP_POISON,
    POWERUP_DEATH,
    POWERUP_SLOWDOWN,
    POWERUP_REVERSE,
]

# Parámetros de Power-ups/Downs
POWERUP_SPAWN_CHANCE = 0.08  # Reducir ligeramente probabilidad
POWERUP_DURATION = 7 # Duración de los power-ups en segundos
INVINCIBILITY_DURATION = 5 # Duración de invencibilidad
MULTIPLIER_DURATION = 10 # Duración del multiplicador de puntuación
REVERSE_DURATION = 7 # Duración del control invertido
SHRINK_AMOUNT = 3 # Cantidad de segmentos a reducir al usar el power-up de reducción de tamaño

# Parámetros de Obstáculos
OBSTACLE_COUNT_NORMAL = 5 # Cantidad de obstáculos en modo normal
OBSTACLE_COUNT_HARD = 10 # Cantidad de obstáculos en modo difícil
OBSTACLE_COUNT_IMPOSSIBLE = 20 # Cantidad de obstáculos en modo imposible

# Parámetros Efecto Niebla (Modo Imposible)
FOG_CHECK_INTERVAL = 2.5 # Intervalo de chequeo de niebla en segundos
FOG_SPAWN_CHANCE = 0.35 # Probabilidad de aparición de niebla
FOG_DURATION = 4 # Duración de la niebla en segundos
FOG_VIEW_RADIUS = BLOCK_SIZE * 6 # Radio de visión clara (radio del círculo de niebla)
FOG_COLOR = (0, 0, 0, 215) # Color de la niebla (RGBA)

# Archivo para guardar la puntuación máxima
HIGHSCORE_FILE = "snake_highscore.txt"

# --- Determinación de Ruta para Highscore (Script vs EXE) ---

# Comprobar si el script está 'congelado' (ejecutándose como .exe de PyInstaller)
if getattr(sys, "frozen", False):
    # Si está congelado, la ruta base es el directorio del ejecutable
    application_path = os.path.dirname(sys.executable)
elif __file__:
    # Si es un script normal .py, la ruta base es el directorio del script
    application_path = os.path.dirname(os.path.abspath(__file__))
else:
    # Fallback: usar el directorio de trabajo actual si no se puede determinar de otra forma
    application_path = os.getcwd()

# Construir la ruta completa y absoluta al archivo de highscore
highscore_filepath = os.path.join(application_path, HIGHSCORE_FILE)

# --- Definición de Colores ---

BACKGROUND_COLOR = (20, 20, 30)  # Fondo del juego
GRID_COLOR = (40, 40, 60)  # Color de la cuadrícula
SCORE_PANEL_BG = (40, 40, 70, 220)  # Fondo del panel de puntuación
SCORE_PANEL_BORDER = (100, 180, 255)  # Borde del panel de puntuación
SCORE_PANEL_BORDER_REVERSE = (255, 0, 100)  # Borde del panel en modo reverso
SCORE_TEXT_COLOR = (255, 255, 255)  # Texto del panel de puntuación
SPEED_TEXT_COLOR = (200, 200, 220)  # Texto de velocidad en el panel
HIGHSCORE_TEXT_COLOR = (255, 223, 0)  # Texto de puntuación máxima
SNAKE_BODY_COLOR = (0, 220, 0)  # Cuerpo de la serpiente
SNAKE_HEAD_COLOR = (0, 120, 0)  # Cabeza de la serpiente
SNAKE_BORDER_COLOR = (0, 50, 0)  # Borde de la serpiente
SNAKE_EYES_COLOR = (255, 255, 255)  # Ojos de la serpiente
FOOD_NORMAL_COLOR = (255, 40, 40)  # Comida normal
FOOD_NORMAL_ALT_COLOR = (180,0,0,)  # Color alternativo para comida normal (efecto pulso)
FOOD_BONUS_COLOR = (255, 215, 0)  # Comida bonus
FOOD_POISON_COLOR = (160, 32, 240)  # Comida venenosa
DEATH_FOOD_COLOR = (124, 252, 0)  # Comida mortal
POWERUP_INVINCIBILITY_COLOR = (0, 206, 209)  # Power-up de invencibilidad
SPEEDUP_COLOR = (0, 255, 255)  # Power-up de aumento de velocidad
SLOWDOWN_COLOR = (210, 105, 30)  # Power-down de reducción de velocidad
SHRINK_COLOR = (144, 238, 144)  # Power-up de reducción de tamaño
MULTIPLIER_COLOR = (211, 211, 211)  # Power-up de multiplicador de puntuación
REVERSE_COLOR = (255, 20, 147)  # Power-down de control invertido
OBSTACLE_COLOR = (100, 100, 110)  # Obstáculos
OBSTACLE_BORDER_COLOR = (60, 60, 70)  # Borde de los obstáculos
OBSTACLE_INNER_COLOR = (80, 80, 90)  # Interior de los obstáculos
TITLE1_COLOR = SNAKE_BODY_COLOR  # Color del título principal
TITLE2_COLOR = (255, 60, 60)  # Color del subtítulo
MENU_TEXT_COLOR = SCORE_TEXT_COLOR  # Texto del menú
MENU_PROMPT_COLOR = SPEED_TEXT_COLOR  # Texto de instrucciones en el menú
GAME_OVER_COLOR = (200, 0, 0)  # Texto de Game Over
INVINCIBLE_FLASH_COLOR = (255, 255, 255)  # Color de parpadeo en modo invencible
ICON_COLOR = (150, 200, 255)  # Color de los íconos en el panel
TEXT_FALLBACK_COLOR = (200, 200, 200)  # Color de texto de respaldo

# --- Configuración de Pantalla y Reloj ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Impossible Snake v1.0")  # Versión actualizada
clock = pygame.time.Clock()

# --- ESTABLECER ICONO DE VENTANA ---

# # Obtener la ruta del directorio donde está el script
base_path = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(base_path, "Snake.png")
try:
    icono = pygame.image.load(icon_path)
    pygame.display.set_icon(icono)
except FileNotFoundError:
    print("Advertencia: El archivo 'Snake.png' no se encontró. Continuando sin icono.")

# --- Carga de Fuentes ---
def get_font(font_names, size, bold=False, italic=False):
    available_fonts = pygame.font.get_fonts()
    preferred = [f for f in font_names if f.lower() in available_fonts]
    if preferred:
        try:
            return pygame.font.SysFont(preferred[0], size, bold, italic)
        except:
            pass
    for name in font_names:
        if name.lower() in available_fonts:
            try:
                return pygame.font.SysFont(name, size, bold, italic)
            except:
                continue
    print(
        f"Advertencia: No se encontraron fuentes {font_names}. Usando fuente por defecto."
    )
    return pygame.font.Font(None, size + 4)


font_title_main = get_font(["impact", "arialblack", "verdana", "arial"], 80)
font_title_sub = get_font(["impact", "arialblack", "verdana", "arial"], 70)
font_game_over = get_font(["impact", "arialblack", "verdana", "arial"], 60)
font_pause = get_font(["impact", "arialblack", "verdana", "arial"], 45)
font_menu = get_font(["consolas", "calibri", "arial"], 35, bold=True)
font_score = get_font(["consolas", "calibri", "arial"], 20, bold=True)
font_small = get_font(["consolas", "calibri", "arial"], 16)


# --- Carga/Manejo de High Score ---
def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                content = f.read().strip()
            return int(content) if content else 0
        except (ValueError, IOError):
            return 0
    else:
        return 0


def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))
    except IOError:
        print(f"Error: No se pudo guardar la puntuación en {HIGHSCORE_FILE}")


high_score = load_highscore()


# --- Generación de Sonido ---
def generate_beep(frequency=440, duration=0.1, volume=0.1):
    if not mixer_initialized:
        return None
    sample_rate = pygame.mixer.get_init()[0]
    num_samples = int(sample_rate * duration)
    amplitude = int(volume * 32767)
    time_points = numpy.linspace(0, duration, num_samples, endpoint=False)
    mono_wave = amplitude * numpy.sin(2 * numpy.pi * frequency * time_points)
    mono_wave_int16 = mono_wave.astype(numpy.int16)
    stereo_wave = numpy.zeros((num_samples, 2), dtype=numpy.int16)
    stereo_wave[:, 0] = mono_wave_int16
    stereo_wave[:, 1] = mono_wave_int16
    try:
        return pygame.sndarray.make_sound(stereo_wave)
    except Exception as e:
        print(f"Error creando sonido con sndarray: {e}")
        return None


sound_eat = generate_beep(920, 0.07, 0.09)
sound_game_over = generate_beep(180, 0.6, 0.25)
sound_powerup_spawn = generate_beep(1300, 0.12, 0.1)
sound_powerup_get = generate_beep(1100, 0.09, 0.15)
sound_powerup_bad = generate_beep(280, 0.18, 0.18)
sound_speed_up = generate_beep(1400, 0.1, 0.12)
sound_slow_down = generate_beep(400, 0.2, 0.18)
sound_shrink = generate_beep(1000, 0.15, 0.12)


# --- Funciones Auxiliares de Dibujo y Lógica ---
def draw_text(text, font, color, surface, x, y, align="topleft"):
    """Dibuja texto con diferentes alineaciones"""
    try:
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        if align == "topleft":
            textrect.topleft = (x, y)
        elif align == "topright":
            textrect.topright = (x, y)
        elif align == "midright":
            textrect.midright = (x, y)
        elif align == "center":
            textrect.center = (x, y)
        elif align == "centerx":
            textrect.centerx = x
            textrect.top = y
        elif align == "centery":
            textrect.centery = y
            textrect.left = x
        else:
            textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
        return textrect  # Devolver rect para usar en subrayado
    except Exception as e:
        fallback_color = (
            (255, 255, 255) if color != (255, 255, 255) else TEXT_FALLBACK_COLOR
        )
        print(
            f"Error dibujando texto: '{text}', Color: {color}, Error: {e}. Usando fallback."
        )
        try:
            textobj = font.render(text, True, fallback_color)
            textrect = textobj.get_rect()
            if align == "topleft":
                textrect.topleft = (x, y)
            elif align == "topright":
                textrect.topright = (x, y)
            elif align == "midright":
                textrect.midright = (x, y)
            elif align == "center":
                textrect.center = (x, y)
            elif align == "centerx":
                textrect.centerx = x
                textrect.top = y
            elif align == "centery":
                textrect.centery = y
                textrect.left = x
            else:
                textrect.topleft = (x, y)
            surface.blit(textobj, textrect)
            return textrect  # Devolver rect también en fallback
        except Exception as e2:
            print(f"Error dibujando texto (fallback): {e2}")
    return None  # Devolver None si hubo error irrecuperable


def draw_background_grid(full_height=False):
    """Dibuja la cuadrícula (completa o solo bajo el panel)"""
    start_y = 0 if full_height else SCORE_PANEL_HEIGHT
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(
            screen, GRID_COLOR, (x, start_y), (x, SCREEN_HEIGHT), GRID_LINE_WIDTH
        )
    first_y = (
        start_y
        if start_y == 0
        else ((start_y + BLOCK_SIZE - 1) // BLOCK_SIZE) * BLOCK_SIZE
    )
    for y in range(first_y, SCREEN_HEIGHT, BLOCK_SIZE):
        if y >= start_y:
            pygame.draw.line(
                screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), GRID_LINE_WIDTH
            )


def draw_score_panel(
    score, current_high_score, speed, is_multiplier_active, is_reverse_active
):
    """Dibuja el panel superior con indicadores"""
    panel_surface = pygame.Surface((SCREEN_WIDTH, SCORE_PANEL_HEIGHT), pygame.SRCALPHA)
    panel_surface.fill(SCORE_PANEL_BG)
    screen.blit(panel_surface, (0, 0))
    border_color = (
        SCORE_PANEL_BORDER_REVERSE
        if is_reverse_active and int(time.time() * 6) % 2 == 0
        else SCORE_PANEL_BORDER
    )
    pygame.draw.line(
        screen,
        border_color,
        (0, SCORE_PANEL_HEIGHT - 1),
        (SCREEN_WIDTH, SCORE_PANEL_HEIGHT - 1),
        2,
    )
    icon_size = BLOCK_SIZE // 2
    icon_padding = 10
    text_icon_gap = 5
    score_y = SCORE_PANEL_HEIGHT * 0.25
    score_icon_x = icon_padding
    score_icon_y = score_y + font_score.get_height() // 2
    pygame.draw.circle(
        screen, ICON_COLOR, (score_icon_x, score_icon_y), icon_size // 2 + 1
    )
    score_text = f"{score}" + (" (x2)" if is_multiplier_active else "")
    draw_text(
        score_text,
        font_score,
        SCORE_TEXT_COLOR,
        screen,
        score_icon_x + icon_size // 2 + text_icon_gap,
        score_y,
        align="topleft",
    )
    speed_y = SCORE_PANEL_HEIGHT * 0.60
    speed_icon_x = icon_padding
    speed_icon_y = speed_y + font_small.get_height() // 2
    bolt_w = icon_size
    bolt_h = icon_size + 2
    bolt_points = [
        (speed_icon_x - bolt_w // 2, speed_icon_y - bolt_h // 4),
        (speed_icon_x + bolt_w // 2, speed_icon_y - bolt_h // 2),
        (speed_icon_x, speed_icon_y),
        (speed_icon_x + bolt_w // 2, speed_icon_y + bolt_h // 4),
        (speed_icon_x - bolt_w // 2, speed_icon_y + bolt_h // 2),
        (speed_icon_x, speed_icon_y),
    ]
    pygame.draw.polygon(screen, ICON_COLOR, bolt_points)
    speed_text = f"{int(speed)}"
    draw_text(
        speed_text,
        font_small,
        SPEED_TEXT_COLOR,
        screen,
        speed_icon_x + bolt_w // 2 + text_icon_gap,
        speed_y,
        align="topleft",
    )
    highscore_y = SCORE_PANEL_HEIGHT * 0.25
    highscore_text = f"{current_high_score}"
    try:
        w, h = font_score.size(highscore_text)
    except Exception:
        w = 50
    highscore_text_x = SCREEN_WIDTH - icon_padding - w
    highscore_icon_x = highscore_text_x - text_icon_gap - (icon_size + 2)
    highscore_icon_y = highscore_y + font_score.get_height() // 2
    star_points = []
    num_points = 5
    outer_radius = icon_size
    inner_radius = icon_size // 2.5
    for i in range(num_points * 2):
        angle = math.pi / num_points * i - math.pi / 2
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = highscore_icon_x + radius * math.cos(angle)
        y = highscore_icon_y + radius * math.sin(angle)
        star_points.append((int(x), int(y)))
    pygame.draw.polygon(screen, HIGHSCORE_TEXT_COLOR, star_points)
    draw_text(
        highscore_text,
        font_score,
        HIGHSCORE_TEXT_COLOR,
        screen,
        highscore_text_x,
        highscore_y,
        align="topleft",
    )


def draw_snake(snake_body, direction, is_invincible):
    """Dibuja la serpiente"""
    if not snake_body:
        return
    head = snake_body[0]
    body_color = SNAKE_BODY_COLOR
    head_color = SNAKE_HEAD_COLOR
    border_color = SNAKE_BORDER_COLOR
    eye_color = SNAKE_EYES_COLOR
    if is_invincible and int(time.time() * 10) % 2 == 0:
        body_color = INVINCIBLE_FLASH_COLOR
        head_color = INVINCIBLE_FLASH_COLOR
        border_color = BACKGROUND_COLOR
        eye_color = BACKGROUND_COLOR
    for segment in snake_body[1:]:
        pygame.draw.rect(
            screen,
            body_color,
            pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE),
        )
        pygame.draw.rect(
            screen,
            border_color,
            pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE),
            1,
        )
    pygame.draw.rect(
        screen, head_color, pygame.Rect(head[0], head[1], BLOCK_SIZE, BLOCK_SIZE)
    )
    pygame.draw.rect(
        screen, border_color, pygame.Rect(head[0], head[1], BLOCK_SIZE, BLOCK_SIZE), 1
    )
    if not (is_invincible and int(time.time() * 10) % 2 == 0):
        eye_size = max(2, BLOCK_SIZE // 4)
        eye_offset_x = BLOCK_SIZE // 4
        eye_offset_y = BLOCK_SIZE // 4
        eye_pos1, eye_pos2 = [0, 0], [0, 0]
        if direction == "UP":
            eye_pos1 = [head[0] + eye_offset_x, head[1] + eye_offset_y]
            eye_pos2 = [
                head[0] + BLOCK_SIZE - eye_offset_x - eye_size,
                head[1] + eye_offset_y,
            ]
        elif direction == "DOWN":
            eye_pos1 = [
                head[0] + eye_offset_x,
                head[1] + BLOCK_SIZE - eye_offset_y - eye_size,
            ]
            eye_pos2 = [
                head[0] + BLOCK_SIZE - eye_offset_x - eye_size,
                head[1] + BLOCK_SIZE - eye_offset_y - eye_size,
            ]
        elif direction == "LEFT":
            eye_pos1 = [head[0] + eye_offset_x, head[1] + eye_offset_y]
            eye_pos2 = [
                head[0] + eye_offset_x,
                head[1] + BLOCK_SIZE - eye_offset_y - eye_size,
            ]
        elif direction == "RIGHT":
            eye_pos1 = [
                head[0] + BLOCK_SIZE - eye_offset_x - eye_size,
                head[1] + eye_offset_y,
            ]
            eye_pos2 = [
                head[0] + BLOCK_SIZE - eye_offset_x - eye_size,
                head[1] + BLOCK_SIZE - eye_offset_y - eye_size,
            ]
        pygame.draw.circle(
            screen,
            eye_color,
            (eye_pos1[0] + eye_size // 2, eye_pos1[1] + eye_size // 2),
            eye_size // 2,
        )
        pygame.draw.circle(
            screen,
            eye_color,
            (eye_pos2[0] + eye_size // 2, eye_pos2[1] + eye_size // 2),
            eye_size // 2,
        )


def draw_food(food_pos):
    """Dibuja la comida normal como círculo"""
    pulse = abs(math.sin(pygame.time.get_ticks() * 0.006))
    try:
        current_color = tuple(
            int(
                FOOD_NORMAL_COLOR[i]
                + (FOOD_NORMAL_ALT_COLOR[i] - FOOD_NORMAL_COLOR[i]) * pulse
            )
            for i in range(3)
        )
    except IndexError:
        current_color = FOOD_NORMAL_COLOR
    center_x = food_pos[0] + BLOCK_SIZE // 2
    center_y = food_pos[1] + BLOCK_SIZE // 2
    radius = BLOCK_SIZE // 2 - 1
    pygame.draw.circle(screen, current_color, (center_x, center_y), radius)


def draw_powerups(powerups):
    """Dibuja todos los powerups/downs activos como círculos"""
    for p in powerups:
        pos = p["pos"]
        ptype = p["type"]
        color = BACKGROUND_COLOR
        if ptype == POWERUP_BONUS:
            color = FOOD_BONUS_COLOR
        elif ptype == POWERUP_POISON:
            color = FOOD_POISON_COLOR
        elif ptype == POWERUP_INVINCIBILITY:
            color = POWERUP_INVINCIBILITY_COLOR
        elif ptype == POWERUP_DEATH:
            color = DEATH_FOOD_COLOR
        elif ptype == POWERUP_SPEEDUP:
            color = SPEEDUP_COLOR
        elif ptype == POWERUP_SLOWDOWN:
            color = SLOWDOWN_COLOR
        elif ptype == POWERUP_SHRINK:
            color = SHRINK_COLOR
        elif ptype == POWERUP_MULTIPLIER:
            color = MULTIPLIER_COLOR
        elif ptype == POWERUP_REVERSE:
            color = REVERSE_COLOR
        center_x = pos[0] + BLOCK_SIZE // 2
        center_y = pos[1] + BLOCK_SIZE // 2
        radius = BLOCK_SIZE // 2 - 1
        pygame.draw.circle(screen, color, (center_x, center_y), radius)
        pygame.draw.circle(screen, BACKGROUND_COLOR, (center_x, center_y), radius, 1)


def draw_obstacles(obstacles):
    """Dibuja los obstáculos con efecto bisel"""
    for obs in obstacles:
        outer_rect = pygame.Rect(obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE)
        inner_rect = pygame.Rect(obs[0] + 2, obs[1] + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4)
        pygame.draw.rect(screen, OBSTACLE_COLOR, outer_rect)
        pygame.draw.rect(screen, OBSTACLE_INNER_COLOR, inner_rect)
        pygame.draw.rect(screen, OBSTACLE_BORDER_COLOR, outer_rect, 1)


def draw_fog_effect(head_pos):
    """Dibuja el efecto de niebla con un círculo de visión clara"""
    fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    fog_surface.fill(FOG_COLOR)
    view_center_x = head_pos[0] + BLOCK_SIZE // 2
    view_center_y = head_pos[1] + BLOCK_SIZE // 2
    # Dibujar círculo transparente (hoyo) - Usar color de fondo con alfa 0
    pygame.draw.circle(
        fog_surface, (0, 0, 0, 0), (view_center_x, view_center_y), FOG_VIEW_RADIUS
    )
    screen.blit(fog_surface, (0, 0))


# --- Pantallas de Menú y Juego ---


def title_screen():
    """Pantalla de título rediseñada (tipográfica)"""
    waiting = True
    title1_y = SCREEN_HEIGHT * 0.30
    title2_y = SCREEN_HEIGHT * 0.45
    prompt_y = SCREEN_HEIGHT * 0.70
    credit_y = SCREEN_HEIGHT - 30
    while waiting:
        screen.fill(BACKGROUND_COLOR)
        draw_background_grid(full_height=True)
        draw_text("SNAKE",font_title_main,TITLE1_COLOR,screen,SCREEN_WIDTH / 2,title1_y,align="center",)
        draw_text("IMPOSIBLE",font_title_sub,TITLE2_COLOR,screen,SCREEN_WIDTH / 2,title2_y,align="center",)
        draw_text("Presiona cualquier tecla para empezar",font_score,MENU_TEXT_COLOR,screen,SCREEN_WIDTH / 2,prompt_y,align="center",)
        draw_text("Creado por Rafael Sanguino",font_small,MENU_PROMPT_COLOR,screen,SCREEN_WIDTH / 2,credit_y,align="center",)
        pygame.display.update()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def difficulty_selection_screen():
    """Pantalla para seleccionar dificultad, incluyendo modo Imposible"""
    selected_option = None
    y_start = SCREEN_HEIGHT * 0.30  # Ajustar Y inicial
    y_step = 60  # Espacio vertical

    while selected_option is None:
        screen.fill(BACKGROUND_COLOR)
        draw_background_grid(full_height=True)
        draw_text(
            "Selecciona Dificultad:",
            font_menu,
            MENU_TEXT_COLOR,
            screen,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.15,
            align="center",
        )
        draw_text(
            "[1] Fácil",
            font_score,
            SNAKE_BODY_COLOR,
            screen,
            SCREEN_WIDTH / 2,
            y_start,
            align="center",
        )
        draw_text(
            "[2] Normal",
            font_score,
            HIGHSCORE_TEXT_COLOR,
            screen,
            SCREEN_WIDTH / 2,
            y_start + y_step,
            align="center",
        )
        draw_text(
            "[3] Difícil",
            font_score,
            FOOD_NORMAL_COLOR,
            screen,
            SCREEN_WIDTH / 2,
            y_start + y_step * 2,
            align="center",
        )

        # Opción Imposible: Mismo tamaño, color rojo, subrayado
        impossible_text = "[4] Imposible"
        text_rect = draw_text(
            impossible_text,
            font_score,
            GAME_OVER_COLOR,
            screen,
            SCREEN_WIDTH / 2,
            y_start + y_step * 3,
            align="center",
        )
        if text_rect:  # Solo dibujar subrayado si el texto se dibujó correctamente
            underline_y = text_rect.bottom + 1  # Posición Y del subrayado
            pygame.draw.line(
                screen,
                GAME_OVER_COLOR,
                (text_rect.left, underline_y),
                (text_rect.right, underline_y),
                2,)  # Línea roja

        draw_text(
            "Presiona ESC o cierra la ventana para salir",
            font_small,
            MENU_PROMPT_COLOR,
            screen,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 50,
            align="center",)
        pygame.display.update()
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    selected_option = (SPEED_EASY, "easy")
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    selected_option = (SPEED_NORMAL, "normal")
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    selected_option = (SPEED_HARD, "hard")
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    selected_option = (SPEED_IMPOSSIBLE, "impossible")
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    return selected_option


def game_over_animation(
    snake_body, current_score, current_speed, is_multiplier_active, is_reverse_active
):
    """Animación de parpadeo al morir (con panel de puntuación)"""
    if sound_game_over:
        sound_game_over.play()
    flash_duration = 0.08
    num_flashes = 6
    original_colors = (SNAKE_BODY_COLOR, SNAKE_HEAD_COLOR, SNAKE_BORDER_COLOR)
    flash_color = GAME_OVER_COLOR
    for i in range(num_flashes * 2):
        is_flash_on = i % 2 == 0
        temp_body, temp_head, temp_border = (
            (flash_color, flash_color, BACKGROUND_COLOR)
            if is_flash_on
            else original_colors
        )
        screen.fill(BACKGROUND_COLOR)
        draw_background_grid(full_height=False)
        # Mostrar panel con estado final durante animación
        draw_score_panel(
            current_score,
            high_score,
            current_speed,
            is_multiplier_active,
            is_reverse_active,
        )
        if snake_body:
            head = snake_body[0]
            for segment in snake_body[1:]:
                pygame.draw.rect(
                    screen,
                    temp_body,
                    pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE),
                )
                pygame.draw.rect(
                    screen,
                    temp_border,
                    pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE),
                    1,
                )
            pygame.draw.rect(
                screen, temp_head, pygame.Rect(head[0], head[1], BLOCK_SIZE, BLOCK_SIZE)
            )
            pygame.draw.rect(
                screen,
                temp_border,
                pygame.Rect(head[0], head[1], BLOCK_SIZE, BLOCK_SIZE),
                1,
            )
        pygame.display.update()
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < flash_duration * 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            clock.tick(60)


def game_over_screen(final_score, current_high_score):
    """Pantalla de Game Over con marcador alineado correctamente"""
    global high_score
    is_new_highscore = False
    if final_score > high_score:
        high_score = final_score
        save_highscore(high_score)
        is_new_highscore = True
    screen.fill(BACKGROUND_COLOR)
    draw_background_grid(full_height=True)
    draw_text(
        "¡GAME OVER!",
        font_game_over,
        GAME_OVER_COLOR,
        screen,
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT * 0.20,
        align="center",
    )
    score_box_y = SCREEN_HEIGHT * 0.38
    score_box_h = 80
    score_box_rect = pygame.Rect(
        SCREEN_WIDTH * 0.2, score_box_y, SCREEN_WIDTH * 0.6, score_box_h
    )
    pygame.draw.rect(screen, SCORE_PANEL_BG, score_box_rect, border_radius=5)
    pygame.draw.rect(screen, SCORE_PANEL_BORDER, score_box_rect, 2, border_radius=5)
    padding_box = 25
    label_x = score_box_rect.left + padding_box
    value_x = score_box_rect.right - padding_box
    line1_y = score_box_y + score_box_h * 0.30
    line2_y = score_box_y + score_box_h * 0.70
    # Usar align="centery" para etiquetas (izquierda) y align="midright" para valores (derecha)
    draw_text(
        "Puntuación Final:",
        font_score,
        MENU_TEXT_COLOR,
        screen,
        label_x,
        line1_y,
        align="centery",
    )
    draw_text(
        f"{final_score}",
        font_score,
        MENU_TEXT_COLOR,
        screen,
        value_x,
        line1_y,
        align="midright",
    )
    if is_new_highscore:
        draw_text(
            "¡NUEVO RÉCORD!:",
            font_score,
            HIGHSCORE_TEXT_COLOR,
            screen,
            label_x,
            line2_y,
            align="centery",
        )
        draw_text(
            f"{high_score}",
            font_score,
            HIGHSCORE_TEXT_COLOR,
            screen,
            value_x,
            line2_y,
            align="midright",
        )
    else:
        draw_text(
            "Puntuación Máxima:",
            font_score,
            HIGHSCORE_TEXT_COLOR,
            screen,
            label_x,
            line2_y,
            align="centery",
        )
        draw_text(
            f"{high_score}",
            font_score,
            HIGHSCORE_TEXT_COLOR,
            screen,
            value_x,
            line2_y,
            align="midright",
        )
    options_y_start = SCREEN_HEIGHT * 0.75
    draw_text(
        "Presiona [R] para Reintentar",
        font_score,
        TITLE1_COLOR,
        screen,
        SCREEN_WIDTH / 2,
        options_y_start,
        align="center",
    )
    draw_text(
        "Presiona [Q] para Salir",
        font_score,
        FOOD_NORMAL_COLOR,
        screen,
        SCREEN_WIDTH / 2,
        options_y_start + 40,
        align="center",
    )
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # 'Q' ahora devuelve 'menu'
                    waiting = False
                    return "menu"
                if event.key == pygame.K_r:  # 'R' devuelve 'retry'
                    waiting = False
                    return "retry"
                if event.key == pygame.K_ESCAPE:  # 'ESC' sigue saliendo
                    pygame.quit()
                    sys.exit()
        clock.tick(15)
    # Si el bucle termina por otra razón (improbable), asumir salida a menú
    return "menu"


def pause_screen():
    """Muestra una pantalla de pausa sobre el juego actual."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    screen.blit(overlay, (0, 0))
    draw_text(
        "PAUSADO",
        font_pause,
        HIGHSCORE_TEXT_COLOR,
        screen,
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT / 2 - 30,
        align="center",
    )
    draw_text(
        "Presiona [P] para continuar",
        font_score,
        MENU_TEXT_COLOR,
        screen,
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT / 2 + 30,
        align="center",
    )
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(15)


# --- Bucle Principal del Juego ---
def game_loop(initial_speed, current_high_score, difficulty_name):
    """Ejecuta una partida completa del juego Snake."""
    # --- Inicialización de variables de la partida ---
    score = 0
    speed = float(initial_speed)
    game_over = False
    paused = False
    death_by_powerup = False
    start_x = (SCREEN_WIDTH // 2 // BLOCK_SIZE) * BLOCK_SIZE
    start_y = (SCREEN_HEIGHT // 2 // BLOCK_SIZE) * BLOCK_SIZE
    snake_pos = [start_x, start_y]
    snake_body = [[snake_pos[0], snake_pos[1]]]
    direction = "RIGHT"
    change_to = direction

    # --- Variables específicas del modo ---
    force_reverse = difficulty_name == "impossible"
    obstacle_count = 0
    if difficulty_name == "normal":
        obstacle_count = OBSTACLE_COUNT_NORMAL
    elif difficulty_name == "hard":
        obstacle_count = OBSTACLE_COUNT_HARD
    elif difficulty_name == "impossible":
        obstacle_count = OBSTACLE_COUNT_IMPOSSIBLE
    allowed_powerups = (
        POWERUP_TYPES_IMPOSSIBLE
        if difficulty_name == "impossible"
        else POWERUP_TYPES_NORMAL
    )

    # --- Generación de Obstáculos ---
    obstacles = []
    valid_obstacle_area = [
        (BLOCK_SIZE, SCREEN_WIDTH - BLOCK_SIZE),
        (SCORE_PANEL_HEIGHT + BLOCK_SIZE, SCREEN_HEIGHT - BLOCK_SIZE),
    ]
    while len(obstacles) < obstacle_count:
        obs_pos = [
            random.randrange(
                valid_obstacle_area[0][0] // BLOCK_SIZE,
                valid_obstacle_area[0][1] // BLOCK_SIZE,
            )
            * BLOCK_SIZE,
            random.randrange(
                valid_obstacle_area[1][0] // BLOCK_SIZE,
                valid_obstacle_area[1][1] // BLOCK_SIZE,
            )
            * BLOCK_SIZE,
        ]
        dist_to_start = abs(obs_pos[0] - start_x) + abs(obs_pos[1] - start_y)
        if (
            obs_pos not in obstacles
            and obs_pos not in snake_body
            and dist_to_start > BLOCK_SIZE * 5
        ):
            obstacles.append(obs_pos)

    # --- Función interna para obtener posición válida de spawn ---
    def get_valid_spawn_pos(current_snake_body, current_obstacles, current_powerups):
        attempts = 0
        while attempts < 100:
            pos = [
                random.randrange(0, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                random.randrange(
                    SCORE_PANEL_HEIGHT // BLOCK_SIZE, (SCREEN_HEIGHT // BLOCK_SIZE)
                )
                * BLOCK_SIZE,
            ]
            powerup_positions = [p["pos"] for p in current_powerups]
            is_on_food = (
                (pos[0] == food_pos[0] and pos[1] == food_pos[1])
                if "food_pos" in locals()
                else False
            )
            if (
                pos not in current_snake_body
                and pos not in current_obstacles
                and pos not in powerup_positions
                and pos[1] >= SCORE_PANEL_HEIGHT
                and not is_on_food
            ):
                return pos
            attempts += 1
        print("Advertencia: No se pudo encontrar una posición válida para spawnear.")
        return [
            random.randrange(0, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
            random.randrange(
                SCORE_PANEL_HEIGHT // BLOCK_SIZE, (SCREEN_HEIGHT // BLOCK_SIZE)
            )
            * BLOCK_SIZE,
        ]

    # --- Inicialización de Comida y Power-ups ---
    active_powerups = []
    food_pos = get_valid_spawn_pos(snake_body, obstacles, active_powerups)
    food_spawned = True
    last_powerup_spawn_time = time.time()
    is_invincible = False
    invincibility_end_time = 0
    is_multiplier_active = False
    multiplier_end_time = 0
    is_reverse_active = False
    reverse_end_time = 0
    is_fog_active = False
    fog_end_time = 0
    fog_activation_timer = time.time()

    # --- Bucle Principal de la Partida ---
    while not game_over:
        current_time = time.time()

        # --- 1. Manejo de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        pause_screen()
                elif not paused:
                    controls_are_reversed = force_reverse or is_reverse_active
                    key_up = pygame.K_DOWN if controls_are_reversed else pygame.K_UP
                    key_down = pygame.K_UP if controls_are_reversed else pygame.K_DOWN
                    key_left = (
                        pygame.K_RIGHT if controls_are_reversed else pygame.K_LEFT
                    )
                    key_right = (
                        pygame.K_LEFT if controls_are_reversed else pygame.K_RIGHT
                    )
                    ord_w = ord("s") if controls_are_reversed else ord("w")
                    ord_s = ord("w") if controls_are_reversed else ord("s")
                    ord_a = ord("d") if controls_are_reversed else ord("a")
                    ord_d = ord("a") if controls_are_reversed else ord("d")
                    if (
                        event.key == key_up or event.key == ord_w
                    ) and direction != "DOWN":
                        change_to = "UP"
                    elif (
                        event.key == key_down or event.key == ord_s
                    ) and direction != "UP":
                        change_to = "DOWN"
                    elif (
                        event.key == key_left or event.key == ord_a
                    ) and direction != "RIGHT":
                        change_to = "LEFT"
                    elif (
                        event.key == key_right or event.key == ord_d
                    ) and direction != "LEFT":
                        change_to = "RIGHT"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if paused:
            clock.tick(15)
            continue

        # --- 2. Actualización de Estado del Juego ---
        direction = change_to
        prev_head_pos = list(snake_pos)
        if direction == "UP":
            snake_pos[1] -= BLOCK_SIZE
        elif direction == "DOWN":
            snake_pos[1] += BLOCK_SIZE
        elif direction == "LEFT":
            snake_pos[0] -= BLOCK_SIZE
        elif direction == "RIGHT":
            snake_pos[0] += BLOCK_SIZE

        if is_invincible:  # Lógica de Wrap
            if snake_pos[0] < 0:
                snake_pos[0] = SCREEN_WIDTH - BLOCK_SIZE
            elif snake_pos[0] >= SCREEN_WIDTH:
                snake_pos[0] = 0
            if snake_pos[1] < SCORE_PANEL_HEIGHT:
                snake_pos[1] = SCREEN_HEIGHT - BLOCK_SIZE
            elif snake_pos[1] >= SCREEN_HEIGHT:
                snake_pos[1] = SCORE_PANEL_HEIGHT

        # Fin de Efectos Temporales
        if is_invincible and current_time > invincibility_end_time:
            is_invincible = False
        if is_multiplier_active and current_time > multiplier_end_time:
            is_multiplier_active = False
        if is_reverse_active and current_time > reverse_end_time:
            is_reverse_active = False
        if difficulty_name == "impossible":  # Lógica de Niebla
            if current_time - fog_activation_timer > FOG_CHECK_INTERVAL:
                fog_activation_timer = current_time
                if not is_fog_active and random.random() < FOG_SPAWN_CHANCE:
                    is_fog_active = True
                    fog_end_time = current_time + FOG_DURATION
            if is_fog_active and current_time > fog_end_time:
                is_fog_active = False

        # --- 3. Lógica de Cuerpo y Colisiones ---
        new_head = list(snake_pos)
        snake_body.insert(0, new_head)
        head_rect = pygame.Rect(snake_pos[0], snake_pos[1], BLOCK_SIZE, BLOCK_SIZE)
        ate_food_this_frame = False

        # Colisión Comida Normal
        food_center_x = food_pos[0] + BLOCK_SIZE // 2
        food_center_y = food_pos[1] + BLOCK_SIZE // 2
        head_center_x = head_rect.centerx
        head_center_y = head_rect.centery
        dist_sq = (head_center_x - food_center_x) ** 2 + (
            head_center_y - food_center_y
        ) ** 2
        food_radius = BLOCK_SIZE // 2 - 1
        if dist_sq < (food_radius * 1.2) ** 2:
            score_increase = 2 if is_multiplier_active else 1
            score += score_increase
            if sound_eat:
                sound_eat.play()
            speed_increase_factor = 0.1 + (speed / 90)
            speed += speed_increase_factor
            food_spawned = False
            ate_food_this_frame = True

        # Colisión Power-ups
        powerup_to_remove = None
        for i, p in enumerate(active_powerups):
            if head_rect.colliderect(
                pygame.Rect(p["pos"][0], p["pos"][1], BLOCK_SIZE, BLOCK_SIZE)
            ):
                ptype = p["type"]
                sound = None  # Resetear sonido por defecto
                if ptype == POWERUP_BONUS:
                    score += 5
                    sound = sound_powerup_get
                elif ptype == POWERUP_POISON:
                    score = max(0, score - 3)
                    sound = sound_powerup_bad
                elif ptype == POWERUP_INVINCIBILITY:
                    is_invincible = True
                    invincibility_end_time = current_time + INVINCIBILITY_DURATION
                    sound = sound_powerup_get
                elif ptype == POWERUP_DEATH:
                    game_over = True
                    death_by_powerup = True
                elif ptype == POWERUP_SPEEDUP:
                    speed += 2
                    sound = sound_speed_up
                elif ptype == POWERUP_SLOWDOWN:
                    speed = max(MIN_SPEED, speed - 2)
                    sound = sound_slow_down
                elif ptype == POWERUP_SHRINK:
                    segments_to_remove = min(SHRINK_AMOUNT, len(snake_body) - 2)
                    if segments_to_remove > 0:
                        [snake_body.pop() for _ in range(segments_to_remove)]
                    sound = sound_shrink
                elif ptype == POWERUP_MULTIPLIER:
                    is_multiplier_active = True
                    multiplier_end_time = current_time + MULTIPLIER_DURATION
                    sound = sound_powerup_get
                elif ptype == POWERUP_REVERSE:
                    is_reverse_active = True
                    reverse_end_time = current_time + REVERSE_DURATION
                    sound = sound_powerup_bad

                if sound:
                    sound.play()
                if not game_over:
                    powerup_to_remove = i
                break

        # Lógica de crecimiento / movimiento y quitar powerup
        if powerup_to_remove is not None:
            if not ate_food_this_frame:
                snake_body.pop()
            active_powerups.pop(powerup_to_remove)
        elif not ate_food_this_frame:
            snake_body.pop()

        # Colisiones de Game Over
        if not game_over and not is_invincible:
            if not (
                0 <= snake_pos[0] < SCREEN_WIDTH
                and SCORE_PANEL_HEIGHT <= snake_pos[1] < SCREEN_HEIGHT
            ):
                game_over = True
            if not game_over and new_head in snake_body[1:]:
                game_over = True
            if not game_over:
                for obs in obstacles:
                    if head_rect.colliderect(
                        pygame.Rect(obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE)
                    ):
                        game_over = True
                        break

        # --- 4. Respawn y Despawn de Elementos ---
        if not food_spawned:
            food_pos = get_valid_spawn_pos(snake_body, obstacles, active_powerups)
            food_spawned = True

        if current_time - last_powerup_spawn_time > 1.5:
            if random.random() < POWERUP_SPAWN_CHANCE:
                ptype_spawn = random.choice(allowed_powerups)  # Usar lista permitida
                ppos = get_valid_spawn_pos(snake_body, obstacles, active_powerups)
                active_powerups.append(
                    {"type": ptype_spawn, "pos": ppos, "spawn_time": current_time}
                )
                if sound_powerup_spawn:
                    sound_powerup_spawn.play()
            last_powerup_spawn_time = current_time

        active_powerups = [
            p
            for p in active_powerups
            if current_time - p["spawn_time"] < POWERUP_DURATION
        ]

        # --- 5. Dibujado ---
        screen.fill(BACKGROUND_COLOR)
        draw_background_grid(full_height=False)
        draw_obstacles(obstacles)
        draw_food(food_pos)
        draw_powerups(active_powerups)
        draw_snake(snake_body, direction, is_invincible)
        if is_fog_active and difficulty_name == "impossible":
            draw_fog_effect(snake_pos)
        # Pasar estado real de inversión (temporal o permanente) para indicador visual
        # El borde solo parpadea si es el powerdown temporal (is_reverse_active) Y NO estamos en modo Imposible (force_reverse)
        draw_score_panel(
            score,
            current_high_score,
            speed,
            is_multiplier_active,
            is_reverse_active and not force_reverse,
        )

        pygame.display.update()
        clock.tick(speed)

    # --- Fin del Bucle Principal (Game Over) ---
    # Pasar estado final de indicadores a la animación
    game_over_animation(
        snake_body,
        score,
        speed,
        is_multiplier_active,
        is_reverse_active and not force_reverse,
    )
    return score


# --- Flujo Principal del Programa ---
if __name__ == "__main__":
    try:
        import numpy
    except ImportError:
        print("Error: La biblioteca 'numpy' es necesaria para generar sonidos.")
        print("Por favor, instálala ejecutando: pip install numpy")
        sys.exit()

    # Variables para recordar la última dificultad seleccionada
    last_selected_speed = None
    last_difficulty_name = None

    title_screen()  # Mostrar título una sola vez

    # Bucle principal que controla reintentos y selección de dificultad
    while True:
        # Si no hay dificultad previa (inicio o tras volver al menú), mostrar selección
        if last_selected_speed is None:
            last_selected_speed, last_difficulty_name = difficulty_selection_screen()

        # Ejecutar una partida con la dificultad actual (nueva o recordada)
        final_score = game_loop(last_selected_speed, high_score, last_difficulty_name)

        # Mostrar pantalla Game Over y obtener acción del usuario
        action = game_over_screen(final_score, high_score)

        if action == "retry":
            # Si reintenta, continuar el bucle; se usarán las 'last_' variables guardadas
            continue
        elif action == "menu":
            # Si vuelve al menú, borrar la dificultad guardada para forzar la selección
            last_selected_speed = None
            last_difficulty_name = None
            continue  # Volver al inicio del bucle (mostrará selección)
        # Si game_over_screen manejó la salida (ESC/Cerrar), el programa ya habrá terminado

    # Salir limpiamente si el bucle termina por alguna razón inesperada (aunque no debería)
    pygame.quit()
    sys.exit()
