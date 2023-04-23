import random
import time
from turtle import Turtle, Screen
from tkinter import messagebox


#screen
screen = Screen()
screen.setup(width=600, height=400)
screen.bgcolor('black')
screen.tracer(0)


#player
player = Turtle()
player.shape("turtle")
player.color('white')
player.penup()
player.goto((0, -180))
player.setheading(90)


def move_left():
    player.setx(player.xcor() - 5)
    bullet.player_x = player.xcor()
    bullet.player_y = player.ycor()


def move_right():
    player.setx(player.xcor() + 5)
    bullet.player_x = player.xcor()
    bullet.player_y = player.ycor()


#scoreboard
scoreboard = Turtle()
scoreboard.color("white")
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.score = 0
with open('highscore.txt', mode="r") as get_score:
    scoreboard.highscore = int(get_score.read())


def update_scoreboard():
    scoreboard.clear()
    scoreboard.goto(210, -160)
    scoreboard.score += 1
    scoreboard.write(f'score:{scoreboard.score}\nhighscore:{scoreboard.highscore}',
                     align="center", font=("Courier", 18, "normal"))


update_scoreboard()


#bullet_system
bullet = Turtle()
bullet.STARTING_POSITION = (0, -500)
bullet.shape("square")
bullet.shapesize(stretch_len=0.8, stretch_wid=0.2)
bullet.color('white')
bullet.penup()
bullet.setheading(90)
bullet.goto(bullet.STARTING_POSITION)
bullet.player_x = 0
bullet.player_y = -180
bullet.bullet_state = 'ready'


def shoot():
    if bullet.bullet_state == 'ready':
        bullet.goto(bullet.player_x, bullet.player_y)
        bullet.bullet_state = 'fire'


#enemies
enemy_x_axis = -270
enemy_y_axis = 180
enemies = []
for i in range(4):
    for j in range(8):
        enemy = Turtle()
        enemy.color("green")
        enemy.shape("turtle")
        enemy.setheading(-90)
        enemy.penup()
        enemy.goto((enemy_x_axis, enemy_y_axis))

        enemies.append(enemy)
        enemy_x_axis += 30
    enemy_x_axis = -270
    enemy_y_axis -= 30

#enemy_bullet_system
enemy_bullet = Turtle()
enemy_bullet.shape("square")
enemy_bullet.shapesize(stretch_len=0.8, stretch_wid=0.2)
enemy_bullet.color('green')
enemy_bullet.penup()
enemy_bullet.setheading(-90)
enemy_bullet.goto((-120, 150))


def enemy_shoot():
    enemy_to_shoot = random.choice(enemies)
    enemy_bullet.goto(enemy_to_shoot.xcor(), enemy_to_shoot.ycor())


#event listeners
screen.listen()
screen.onkeypress(key="a", fun=move_left)
screen.onkeypress(key="d", fun=move_right)
screen.onkeypress(key="space", fun=shoot)

#game
crossed_right = False
has_1st_shot = False
game_is_on = True
speed = 0.1
i = 0
while game_is_on:
    time.sleep(speed)
    if enemies == []:
        messagebox.showinfo(
            "You won!", f"Your score was: {scoreboard.score}, great job!")
        game_is_on = False

    #enemies mechanics
    for enemy in enemies:
        if not crossed_right:
            enemy.setx(enemy.xcor() + 5)
            if enemies[-1].xcor() > 280:
                crossed_right = True
        elif crossed_right:
            enemy.setx(enemy.xcor() - 5)
            if enemies[0].xcor() < -280:
                crossed_right = False

    #firing mechanic
    if bullet.bullet_state == 'fire':
        bullet.forward(20)

        if bullet.ycor() > 210:
            bullet.goto(bullet.STARTING_POSITION)
            bullet.bullet_state = 'ready'

        for enemy in enemies:
            if bullet.distance(enemy) < 20:
                enemy.reset()
                enemies.remove(enemy)
                enemy.goto(-500, -500)
                bullet.goto(bullet.STARTING_POSITION)
                bullet.bullet_state = 'ready'
                update_scoreboard()
    if i % 5 == 0:
        if enemy_bullet.ycor() < -310:
            enemy_shoot()
            has_1st_shot = True
    enemy_bullet.forward(20)

    if enemy_bullet.distance(player) < 20:
        messagebox.showinfo(
            "Game is Over!", f"Your score was: {scoreboard.score}, great job!")
        game_is_on = False
        if scoreboard.score > scoreboard.highscore:
            scoreboard.highscore = scoreboard.score
            with open("finished-projects/81-100. [PRO]/94. [Game] Space Invaders/highscore.txt", mode="w") as score_txt:
                score_txt.write(str(scoreboard.highscore))

    speed *= 0.999
    i += 1
    screen.update()
screen.exitonclick()
