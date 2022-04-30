import pygame
import sys
import random
from words import *

pygame.init()

# Constants

ancho, alto = 633, 900

pantallaJuego = pygame.display.set_mode((ancho, alto))
fondo = pygame.image.load("assets/casillas.png")
fondo_rect = fondo.get_rect(center=(317, 300))
icono = pygame.image.load("assets/icono.png")

pygame.display.set_caption("Wordle")
pygame.display.set_icon(icono)

verde = "#6aaa64"
amarillo = "#c9b458"
gris = "#787c7e"

long = 5
filename = "palabras.txt"

def read_words(filename, long): #convierte el fichero de palabras en una lista de palabras de longitud 5
    lista = []
    f = open(filename, 'r')
    linea = f.readline()
    while linea != '':
        if len(linea) - 1 == long:
            lista.append(linea.strip())
        linea = f.readline()
    f.close()
    return lista
    
def elegir_palabra(filename, long): #elige una palabra aleatoria de la lista
    lista = read_words(filename, long)
    a = random.randint(0, len(lista) - 1)
    palabra = lista[a]
    return palabra

solucion = elegir_palabra(filename, long)

abecedario = ["QWERTYUIOP", "ASDFGHJKLÑ", "ZXCVBNM"]

GUESSED_LETTER_FONT = pygame.font.Font("assets/animeace2_bld.otf", 50)
AVAILABLE_LETTER_FONT = pygame.font.Font("assets/animeace2_bld.otf", 25)

pantallaJuego.fill("white")
pantallaJuego.blit(fondo, fondo_rect)
pygame.display.update()

espacioLetrasx = 85
espacioLetrasy = 12
tamanioLetra = 75
n_intentos = 0
intentos = [[]] * 6
intentoActual = []
intentoActual_string = ""
letraActualFondo_x = 110
indicators = []
resultado = ""

class Letra:
    def __init__(self, letra, posicionFondo):
        # Initializes all the variables, including text, color, position, size, etc.
        self.colorFondoLetra = "white"
        self.colorFondo = "white"
        self.colorLetra = "black"
        self.posicionFondo = posicionFondo
        self.fondox = posicionFondo[0]
        self.fondoy = posicionFondo[1]
        self.fondo_rect = (posicionFondo[0], self.fondoy, tamanioLetra, tamanioLetra)
        self.letra = letra
        self.posicionLetra = (self.fondox+36, self.posicionFondo[1]+34)
        self.letra_surface = GUESSED_LETTER_FONT.render(self.letra, True, self.colorLetra)
        self.letra_rect = self.letra_surface.get_rect(center=self.posicionLetra)

    def draw(self):
        pygame.draw.rect(pantallaJuego, self.colorFondo, self.fondo_rect)
        if self.colorFondo == "white":
            pygame.draw.rect(pantallaJuego, "#878a8c", self.fondo_rect, 3)
        pantallaJuego.blit(self.letra_surface, self.letra_rect)
        pygame.display.update()

    def delete(self):
        pygame.draw.rect(pantallaJuego, "white", self.fondo_rect)
        pygame.draw.rect(pantallaJuego, "#878a8c",self.fondo_rect, 3)
        pygame.display.update()

class Indicator:
    def __init__(self, x, y, letra):
        # Initializes variables such as color, size, position, and letter.
        self.x = x
        self.y = y
        self.letra = letra
        self.rect = (self.x, self.y, 57, 75)
        self.colorFondo = "white"

    def draw(self):
        # Puts the indicator and its text on the screen at the desired position.
        pygame.draw.rect(pantallaJuego, self.colorFondo, self.rect)
        self.letra_surface = AVAILABLE_LETTER_FONT.render(self.letra, True, "black")
        self.letra_rect = self.letra_surface.get_rect(center=(self.x+27, self.y+30))
        pantallaJuego.blit(self.letra_surface, self.letra_rect)
        pygame.display.update()
        
indicator_x, indicator_y = 20, 600

for i in range(3):
    for letra in abecedario[i]:
        new_indicator = Indicator(indicator_x, indicator_y, letra)
        indicators.append(new_indicator)
        new_indicator.draw()
        indicator_x += 60
    indicator_y += 100
    if i == 0:
        indicator_x = 50
    elif i == 1:
        indicator_x = 105

def compruebaIntento(guess_to_check):
    global intentoActual, intentoActual_string, n_intentos, letraActualFondo_x, resultado
    game_decided = False
    for i in range(5):
        lowercase_letter = guess_to_check[i].letra.lower()
        if lowercase_letter in solucion:
            if lowercase_letter == solucion[i]:
                guess_to_check[i].colorFondo = verde
                for indicator in indicators:
                    if indicator.letra == lowercase_letter.upper():
                        indicator.colorFondo = verde
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                if not game_decided:
                    resultado = "W"
            else:
                guess_to_check[i].colorFondo = amarillo
                for indicator in indicators:
                    if indicator.letra == lowercase_letter.upper():
                        indicator.colorFondo = amarillo
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                resultado = ""
                game_decided = True
        else:
            guess_to_check[i].colorFondo = "red"
            for indicator in indicators:
                if indicator.letra == lowercase_letter.upper():
                    indicator.colorFondo = "red"
                    indicator.draw()
            guess_to_check[i].text_color = "white"
            resultado = ""
            game_decided = True
        guess_to_check[i].draw()
        pygame.display.update()
    
    n_intentos += 1
    intentoActual = []
    intentoActual_string = ""
    letraActualFondo_x = 110

    if n_intentos == 6 and resultado == "":
        resultado = "L"

def juegaDeNuevo():
    pygame.draw.rect(pantallaJuego, "white", (10, 600, 1000, 600))
    juegaDeNuevo_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    juegaDeNuevo_text = juegaDeNuevo_font.render("ENTER to para volver a jugar", True, "black")
    juegaDeNuevo_rect = juegaDeNuevo_text.get_rect(center=(ancho/2, 700))
    word_was_text = juegaDeNuevo_font.render(f"La palabra era {solucion}!", True, "black")
    word_was_rect = word_was_text.get_rect(center=(ancho/2, 650))
    pantallaJuego.blit(word_was_text, word_was_rect)
    pantallaJuego.blit(juegaDeNuevo_text, juegaDeNuevo_rect)
    pygame.display.update()

def reset():
    global n_intentos, solucion, intentos, intentoActual, intentoActual_string, resultado
    pantallaJuego.fill("white")
    pantallaJuego.blit(fondo, fondo_rect)
    n_intentos = 0
    solucion = elegir_palabra(filename, long)
    intentos = [[]] * 6
    intentoActual = []
    intentoActual_string = ""
    resultado = ""
    pygame.display.update()
    for indicator in indicators:
        indicator.colorFondo = "white"
        indicator.draw()

def crearnuevaLetra():
    global intentoActual_string, letraActualFondo_x
    intentoActual_string += pulsaLetra
    nuevaLetra = Letra(pulsaLetra, (letraActualFondo_x, n_intentos*100+espacioLetrasy))
    letraActualFondo_x += espacioLetrasx
    intentos[n_intentos].append(nuevaLetra)
    intentoActual.append(nuevaLetra)
    for intento in intentos:
        for letra in intento:
            nuevaLetra.draw()

def borrarLetra():
    global intentoActual_string, letraActualFondo_x
    intentos[n_intentos][-1].delete()
    intentos[n_intentos].pop()
    intentoActual_string = intentoActual_string[:-1]
    intentoActual.pop()
    letraActualFondo_x -= espacioLetrasx

while True:
    if resultado != "":
        juegaDeNuevo()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if resultado != "":
                    reset()
                else:
                    if len(intentoActual_string) == 5 and intentoActual_string.lower() in read_words(filename, long):
                        compruebaIntento(intentoActual)
            elif event.key == pygame.K_BACKSPACE:
                if len(intentoActual_string) > 0:
                    borrarLetra()
            else:
                pulsaLetra = event.unicode.upper()
                if pulsaLetra in "QWERTYUIOPASDFGHJKLÑZXCVBNM" and pulsaLetra != "":
                    if len(intentoActual_string) < 5:
                        crearnuevaLetra()
