import pygame
import chess

# Configuración básica
ANCHO_VENTANA = 640
ALTO_VENTANA = 640
FILAS, COLUMNAS = 8, 8
TAM_CELDA = ANCHO_VENTANA // COLUMNAS

# Colores
BLANCO = (245, 245, 245)
GRIS = (125, 135, 150)
AZUL = (50, 130, 200)


# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tablero de Ajedrez 8x8")

# Piezas

# Blancas
rey_blanco = pygame.image.load('piezas imagenes/rey_blanco.png')
rey_blanco = pygame.transform.scale(rey_blanco, (TAM_CELDA, TAM_CELDA))  # ajusta tamaño a la celda
reina_blanca = pygame.image.load('piezas imagenes/reina_blanco.png')
reina_blanca = pygame.transform.scale(reina_blanca, (TAM_CELDA, TAM_CELDA))  
alfil_blanco = pygame.image.load('piezas imagenes/alfil_blanco.png')
alfil_blanco = pygame.transform.scale(alfil_blanco, (TAM_CELDA, TAM_CELDA)) 
alfil_blanco2 = pygame.image.load('piezas imagenes/alfil_blanco.png')
alfil_blanco2 = pygame.transform.scale(alfil_blanco2, (TAM_CELDA, TAM_CELDA))   
torre_blanca = pygame.image.load('piezas imagenes/torre_blanco.png')
torre_blanca = pygame.transform.scale(torre_blanca, (TAM_CELDA, TAM_CELDA))  
torre_blanca2 = pygame.image.load('piezas imagenes/torre_blanco.png')
torre_blanca2 = pygame.transform.scale(torre_blanca2, (TAM_CELDA, TAM_CELDA))
caballo_blanco = pygame.image.load('piezas imagenes/caballo_blanco.png')
caballo_blanco = pygame.transform.scale(caballo_blanco, (TAM_CELDA, TAM_CELDA))  
caballo_blanco2 = pygame.image.load('piezas imagenes/caballo_blanco.png')
caballo_blanco2 = pygame.transform.scale(caballo_blanco2, (TAM_CELDA, TAM_CELDA)) 
peon_blanco = pygame.image.load('piezas imagenes/peon_blanco.png')
peon_blanco = pygame.transform.scale(peon_blanco, (TAM_CELDA, TAM_CELDA))  

#negras
rey_negro = pygame.image.load('piezas imagenes/rey_negro.png')
rey_negro = pygame.transform.scale(rey_negro, (TAM_CELDA, TAM_CELDA)) 
reina_negra = pygame.image.load('piezas imagenes/reina_negro.png')
reina_negra = pygame.transform.scale(reina_negra, (TAM_CELDA, TAM_CELDA))  
alfil_negro = pygame.image.load('piezas imagenes/alfil_negro.png')
alfil_negro = pygame.transform.scale(alfil_negro, (TAM_CELDA, TAM_CELDA))  
alfil_negro2 = pygame.image.load('piezas imagenes/alfil_negro.png')
alfil_negro2 = pygame.transform.scale(alfil_negro2, (TAM_CELDA, TAM_CELDA))
torre_negra = pygame.image.load('piezas imagenes/torre_negro.png')
torre_negra = pygame.transform.scale(torre_negra, (TAM_CELDA, TAM_CELDA))
torre_negra2 = pygame.image.load('piezas imagenes/torre_negro.png')
torre_negra2 = pygame.transform.scale(torre_negra2, (TAM_CELDA, TAM_CELDA))  
caballo_negro = pygame.image.load('piezas imagenes/caballo_negro.png')
caballo_negro = pygame.transform.scale(caballo_negro, (TAM_CELDA, TAM_CELDA))
caballo_negro2 = pygame.image.load('piezas imagenes/caballo_negro.png')
caballo_negro2 = pygame.transform.scale(caballo_negro, (TAM_CELDA, TAM_CELDA))  
peon_negro = pygame.image.load('piezas imagenes/peon_negro.png')
peon_negro = pygame.transform.scale(peon_negro, (TAM_CELDA, TAM_CELDA))  

# Control de ejecución
running = True
celda_seleccionada = None

# Función para dibujar el tablero
def dibujar_tablero():
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            color = BLANCO if (fila + col) % 2 == 0 else GRIS
            rect = pygame.Rect(col * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA)
            pygame.draw.rect(ventana, color, rect)

    if celda_seleccionada:
        fila, col = celda_seleccionada
        rect = pygame.Rect(col * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA)
        pygame.draw.rect(ventana, AZUL, rect, 4)  # borde azul
        ventana.blit(alfil_negro, (col * TAM_CELDA, fila * TAM_CELDA))

# Bucle principal
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            fila = y // TAM_CELDA
            col = x // TAM_CELDA
            celda_seleccionada = (fila, col)

    dibujar_tablero()
    pygame.display.flip()

pygame.quit()
