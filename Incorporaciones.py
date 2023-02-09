#!/usr/bin/python3

import turtle
from random import randint


def ship_right():
    """
    Funcion para que la nave se mueva a la dereha.
    Actualmente se activa con la flecha derecha.
    """
    x = ship.xcor()  # Coordenada x actual
    if x >= 230:
        ship.setx(230)  # Condicion para no salirse del borde derecho
    else:
        ship.setx(x + 10)  # Mueve la nave 10 pixeles a la derecha


def ship_left():
    """
    Funcion para para que la nave se mueva a la izquierda.
    Actualmente se activa con la flecha izquierda.
    """
    x = ship.xcor()  # Coordenada x actual
    if x <= -230:
        ship.setx(-230)  # Condicion para no salirse del borde izquierdo
    else:
        ship.setx(x - 10)  # Mueve la nave 10 pixeles a la izquierda


def ship_weapons():
    """
    Función para que el proyectil sea disparado por la nave.
    Actualmente se activa con la barra espaciadora.
    """
    # Variable GLOBAL necesaria para trackear el estado del proyectil
    global avaiable

    # Solo dispara si el proyectil está disponible
    if avaiable is True:
        # NOTA: El track se mueve dentro de la fución para corregir error
        # de posición a la hora del disparo.
        proyectile.goto(ship.xcor(),
                        ship.ycor()+10)  # Regresa a la punta de la nave
        avaiable = False


def alien_move(alien):
    """
    Función de movimiento de los enemigos.
    Se activa constantmente durante el loop principal del juego.

    alien: Objeto.turtle() correspondiente a un enemigo
    """
    y = alien.ycor()  # Coordenada x del alien
    x = alien.xcor()  # Coordenada y del alien

    # Determina la dirección del movimiento del alien.
    # direction = 1: se mueve a la derecha
    # direction = -1: se mueve a la izquierda
    direction = alien.direction

    # Velocidad horizontal del alien
    avance = 0.05

    # Se asegura de que el alien este en la parte superior de la pantalla
    while y > 240:
        alien.forward(avance)
        window.update()
        y = alien.ycor()

    # Da movimiento al alien una vez está en posición
    alien.setx(x + direction*avance)

    # Condición de limite derecho en la pantalla
    if alien.xcor() >= 230:
        y = alien.ycor()
        alien.goto(230, y-40)  # Baja al alien 40 pixeles en y
        alien.direction = -1  # Cambia la dirección del alien
    # Condición de limite derecho en la pantalla
    elif alien.xcor() <= -230:
        y = alien.ycor()
        alien.goto(-230, y-40)  # Baja al alien 40 pixeles en y
        alien.direction = 1  # Cambia la dirección del alien


if __name__ == "__main__":
    # Creación de la ventana del juego
    window = turtle.Screen()
    window.title("Alien Invaders")
    window.setup(width=500, height=500)  # Unidades en pixeles
    window._bgcolor("black")
    window.tracer(0)

    # Creación de la nave del usuario
    ship = turtle.Turtle()
    ship.speed(0)
    ship.shape("arrow")
    ship.color("white")
    ship.left(90)
    ship.penup()
    ship.goto(0, -240)  # Posicion inicial al centro y abajo

    # Creación del proyectil que dispara el usuario
    # Fue necesario sacarlo de la función ya que sino el loop principal crashea
    proyectile = turtle.Turtle()
    proyectile.hideturtle()  # Inicialmente oculto (No ha disparado)
    proyectile.speed(0)
    proyectile.shape("circle")
    proyectile.color("red")
    proyectile.turtlesize(0.14, 0.52)
    proyectile.left(90)
    proyectile.penup()
    proyectile.goto(ship.xcor(),
                    ship.ycor()+10)  # Ubicado en la punta de la nave
    avaiable = True  # Disponibilidad del proyectil. Disponible al inicio

    # Creación del enemigo
    alien = turtle.Turtle()
    alien.speed(0)
    alien.shape("triangle")
    alien.color("green")
    alien.right(90)
    alien.penup()
    alien.goto(0, 260)  # Posicion inicial al centro y abajo
    alien.direction = 1  # Inicialmente se mueve a la derecha

    # Para que la ventana rastree los inputs del teclado
    window.listen()

    # Asociacion del teclado con el movimiento de la nave
    window.onkeypress(ship_right, "Right")  # Derecha
    window.onkeypress(ship_left, "Left")  # Izquierda
    window.onkeypress(ship_weapons, "space")  # Disparo

    while True:
        window.update()

        alien_move(alien)

        if avaiable is False:
            avance = 0.05  # Velocidad del proyectil
            proyectile.showturtle()  # Vuelve visible el proyectil
            proyectile.forward(avance)
            if proyectile.ycor() >= 250:
                # NOTA: El track del proyectil se traslado a la función
                # ship_weapons() para corregir error de posición
                proyectile.hideturtle()  # Vuelve a ocultar el proyectil
                avaiable = True  # Vuelve a estar disponible

        # Situación de Game Over
        if alien.ycor() < ship.ycor():
            alien.goto(0, 0)  # Cambiar cuando este listo

        # Bases de la colisión alien-proyectil
        if (alien.xcor() >= -10 and alien.xcor() <= 10) and (alien.ycor() >= -10 and alien.ycor() <= 10):
            y = randint(260, 560)
            x = alien.xcor()
            alien.goto(x, y)
