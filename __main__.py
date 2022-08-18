#!/usr/bin/python3

# import required modules
import turtle
import time
import random
import json
import playsound
import sys

random.seed(int(time.time()))

try:
    f = open("gameinfo.json")
    gameinfo = json.load(f)
    f.close()
except:
    try:
        f = open("snake/gameinfo.json")
        gameinfo = json.load(f)
        f.close()
    except Exception as e:
        exit("Error occured: {e}")

SOUND = "on"
delay = 0.07
score = 0
high_score = int(gameinfo['highscore'])
for arg in sys.argv:
    if arg == "--nosound":
        SOUND = "off"



# Creating a window screen
wn = turtle.Screen()
wn.delay(0)
wn.title("Snake Game")
wn.bgcolor("#6e7fa0")
# the width and height can be put as user's choice
wn.setup(width=600, height=600)
wn.tracer(0)

# head of the snake
head = turtle.Turtle()
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# food in the game
food = turtle.Turtle()
#colors = random.choice(['red', 'green', 'black']) [removed]
shapes = random.choice(['square', 'triangle', 'circle'])
food.speed(0)
food.shape(shapes)
food.color("black")
food.penup()
food.goto(0, 100)

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 250)
pen.write(f"0 (High Score {high_score})", align="center",
        font=("candara", 24, "bold"))



# assigning key directions
def group():
    if head.direction != "down":
        head.direction = "up"


def godown():
    if head.direction != "up":
        head.direction = "down"


def goleft():
    if head.direction != "right":
        head.direction = "left"


def goright():
    if head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y-20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x-20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x+20)

def quit_game():
    wn.bye()

wn.listen()
wn.onkeypress(group, "w")
wn.onkeypress(godown, "s")
wn.onkeypress(goleft, "a")
wn.onkeypress(goright, "d")
#adding arrow keys, too
wn.onkeypress(group, "Up")
wn.onkeypress(godown, "Down")
wn.onkeypress(goleft, "Left")
wn.onkeypress(goright, "Right")
#exit game
wn.onkeypress(quit_game, "Escape")

segments = []

def addTails():
    for i in range(9):
        startingTail = turtle.Turtle()
        startingTail.speed(0)
        startingTail.shape("square")
        startingTail.color("black")
        startingTail.penup()
        segments.append(startingTail)

addTails()

# Main Gameplay
while True:
    wn.update()
    if len(segments) < 1:
        addTails()
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        if head.direction != "stop" and high_score > score and SOUND == "on":
            try:
                playsound.playsound("gameover.wav")
            except:
                try:
                    playsound.playsound("snake/gameover.wav")
                except Exception as e:
                    print(e)
        if head.direction != "stop" and high_score <= score and SOUND == "on":
            try:
                playsound.playsound("highscore.wav")
            except:
                try:
                    playsound.playsound("snake/highscore.wav")
                except Exception as e:
                    print(e)
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "Stop"
        shapes = random.choice(['square', 'circle'])
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        #addTails()
        score = 0
        pen.clear()
        pen.write("{} (High Score {})".format(
            score, high_score), align="center", font=("candara", 24, "bold"))
    if head.distance(food) < 20:
        if SOUND == "on":
            try:
                playsound.playsound("food.wav")
            except:
                try:
                    playsound.playsound("snake/food.wav")
                except Exception as e:
                    print(e)
        x = random.randint(-270, 270)
        y = random.randint(-270, 270)
        shapes = random.choice(['square', 'circle'])
        food.shape(shapes)
        food.goto(x, y)
        # Adding segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("black") # tail color
        new_segment.penup()
        segments.append(new_segment)
        score += 7
        if score > high_score:
            high_score = score
            f = open("gameinfo.json", 'w')
            gameinfo["highscore"] = str(high_score)
            f.write(json.dumps(gameinfo))
            f.close()
        pen.clear()
        pen.write("{} (High Score {}) ".format(
            score, high_score), align="center", font=("candara", 24, "bold"))
    # Checking for head collisions with body segments
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)
    move()
    for segment in segments:
        if segment.distance(head) < 20:
            if head.direction != "stop" and head.pos() != (0, 0) and high_score > score and SOUND == "on":
                try:
                    playsound.playsound("gameover.wav")
                except:
                    try:
                        playsound.playsound("snake/gameover.wav")
                    except Exception as e:
                        print(e)
            if head.direction != "stop" and head.pos() != (0, 0) and high_score <= score and SOUND == "on":
                try:
                    playsound.playsound("highscore.wav")
                except:
                    try:
                        playsound.playsound("snake/highscore")
                    except Exception as e:
                        print(e)
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            shapes = random.choice(['square', 'circle'])
            for segment in segments:
                segment.goto(1000, 1000)
                segment.ht()
            segment.clear()
            segments.clear()
            score = 0
            pen.clear()
            pen.write("{} (High Score {})".format(
                score, high_score), align="center", font=("candara", 24, "bold"))
    time.sleep(delay)

wn.mainloop()
