import turtle
import random

import _tkinter

fontFace = "Arial"
fontSize = 24
textAlign = "center"


class Pong:
    def __init__(self, screenWidth: int = 800, screenHeight: int = 600, bgcolor: str = "black", ballSpeedSet: bool = True, ballSpeed: int = 5, playerSet: bool = False, player1: str = "Player 1", player2: str = "Player 2", player1Color: str = "red", player2Color: str = "blue"):

        self.screen_width = screenWidth
        self.screen_height = screenHeight
        self.screen = turtle.Screen()
        self.screen.title("Pong with Python Turtle 0.0.1")

        if playerSet == False:
            self.player1 = self.screen.textinput(
                "Player 1", "Who is player 1?")
            self.player2 = self.screen.textinput(
                "Player 2", "Who is player 2?")
            if self.player1 is None:
                self.player1 = player1
            elif self.player2 is None:
                self.player2 = player2
        else:
            self.player1 = player1
            self.player2 = player2

        if ballSpeedSet == False:
            self.ballSpeed = self.screen.textinput(
                "Ball Speed", "What is the ball speed?")
            if self.ballSpeed is not None:
                self.ballSpeed = int(self.ballSpeed)
        else:
            self.ballSpeed = ballSpeed

        # Set up game screen
        self.screen.setup(self.screen_width, self.screen_height)

        # Set game screen background color
        self.screen.bgcolor(bgcolor)

        self.points = {
            self.player1: 0,
            self.player2: 0
        }

        self.leftBound = -(self.screen.window_width()/2)
        self.rightBound = (self.screen.window_width()/2)
        self.upperBound = (self.screen.window_height()/2)
        self.lowerBound = -(self.screen.window_height()/2)
        self.movePaddleBy = 20

        # Creating the left paddle
        self.paddle1 = turtle.Turtle()
        self.initLeftPaddle(player1Color)

        # Creating the right paddle
        self.paddle2 = turtle.Turtle()
        self.initRightPaddle(player2Color)

        # Creating the ball
        self.ball = turtle.Turtle()
        self.initBall()

        self.score_display = turtle.Turtle()
        self.initScoreDisplay()

    def __str__(self) -> str:
        return f"{self.player1}: {self.points[self.player1]}  {self.player2}: {self.points[self.player2]}"

    def initLeftPaddle(self, color: str = "red", width: int = 5, length: int = 1):
        self.paddle1.shape("square")
        self.paddle1.color(color)
        self.paddle1.shapesize(
            stretch_wid=width, stretch_len=length)  # make paddle wider
        self.paddle1.penup()
        self.paddle1.goto(self.leftBound + 50, 0)
        self.paddle1.dy = 0

    def initRightPaddle(self, color: str = "blue", width: int = 5, length: int = 1):
        self.paddle2.shape("square")
        self.paddle2.color(color)
        self.paddle2.shapesize(
            stretch_wid=width, stretch_len=length)  # make paddle wider
        self.paddle2.penup()
        self.paddle2.goto(self.rightBound - 50, 0)
        self.paddle2.dy = 0

    def initBall(self, color: str = "white"):
        self.ball.shape("circle")
        self.ball.color(color)
        self.ball.penup()
        self.ball.goto(0, 0)
        self.ball.dx = self.ballSpeed * random.choice([-1, 1])
        self.ball.dy = self.ballSpeed * random.choice([-1, 1])

    def initScoreDisplay(self, color: str = "white"):
        self.score_display.color(color)
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(0, self.upperBound - 40)
        self.score_display.write(f"{self.player1}: {self.points[self.player1]}  {self.player2}: {self.points[self.player2]}",
                                 align=textAlign, font=(fontFace, fontSize, "normal"))

    def updateScoreDisplay(self):
        # Update score display
        self.score_display.clear()
        self.score_display.write(f"{self.player1}: {self.points[self.player1]}  {self.player2}: {self.points[self.player2]}", align=textAlign, font=(
            fontFace, fontSize, "normal"))

    def moveBall(self):
        self.ball.setx(self.ball.xcor() + self.ball.dx)
        self.ball.sety(self.ball.ycor() + self.ball.dy)

    def paddle1_up(self):
        # Function to move paddle1 up
        self.paddle1.sety(self.paddle1.ycor()+self.movePaddleBy)

    def paddle1_down(self):
        # Function to move paddle1 down
        self.paddle1.sety(self.paddle1.ycor()-self.movePaddleBy)

    def paddle2_up(self):
        # Function to move paddle2 up
        self.paddle2.sety(self.paddle2.ycor()+self.movePaddleBy)

    def paddle2_down(self):
        # Function to move paddle2 down
        self.paddle2.sety(self.paddle2.ycor()-self.movePaddleBy)

    def setKeyboardBindings(self):
        # Set up keyboard bindings
        self.screen.listen()
        self.screen.onkeypress(self.paddle1_up, "w")
        self.screen.onkeypress(self.paddle1_down, "s")
        self.screen.onkeypress(self.paddle2_up, "Up")
        self.screen.onkeypress(self.paddle2_down, "Down")

    def checkCollisionWithLeftPaddle(self) -> bool:
        return self.ball.xcor() < (self.paddle1.xcor() + 10) and self.ball.xcor() > self.paddle1.xcor() and self.ball.ycor() < self.paddle1.ycor() + 50 and self.ball.ycor() > self.paddle1.ycor() - 50

    def checkCollisionWithRightPaddle(self) -> bool:
        return (self.ball.xcor() > (self.paddle2.xcor() - 10) and self.ball.xcor() < self.paddle2.xcor()) and (self.ball.ycor() < self.paddle2.ycor() + 50 and self.ball.ycor() > self.paddle2.ycor() - 50)

    def collisionWithPaddles(self):
        # Check for ball collision with paddles
        if self.checkCollisionWithRightPaddle():
            self.ball.setx((self.paddle2.xcor() - 10))
            self.ball.dx *= -1
        elif self.checkCollisionWithLeftPaddle():
            self.ball.setx((self.paddle1.xcor() + 10))
            self.ball.dx *= -1

    def goingOutOfScreen(self):
        # Check for ball going off screen
        if self.ball.xcor() > (self.rightBound - 10) or self.ball.xcor() < (self.leftBound + 10):
            if self.ball.xcor() > (self.rightBound - 10):
                self.ball.goto(0, 0)    # reset position
                self.ball.dx *= -1
                self.points[self.player1] += 1
            elif self.ball.xcor() < (self.leftBound + 10):
                self.ball.goto(0, 0)    # reset position
                self.ball.dx *= -1
                self.points[self.player2] += 1
            self.updateScoreDisplay()

    def collisionWithScreen(self):
        # Check for ball colliding with top or bottom of screen
        if self.ball.ycor() > (self.upperBound - 10):
            self.ball.sety((self.upperBound - 10))
            self.ball.dy *= -1
        elif self.ball.ycor() < (self.lowerBound + 10):
            self.ball.sety((self.lowerBound + 10))
            self.ball.dy *= -1

    def getWinner(self) -> str:
        if self.points[self.player1] > self.points[self.player2]:
            return self.player1
        elif self.points[self.player2] > self.points[self.player1]:
            return self.player2
        else:
            return None

    def displayGameOverScreen(self):
        self.ball.hideturtle()

        # Game over screen
        game_over_display = turtle.Turtle()
        game_over_display.color("white")
        game_over_display.penup()
        game_over_display.hideturtle()
        game_over_display.goto(0, 0)
        game_over_display.write(
            f"Game Over! {self.getWinner()} wins!", align=textAlign, font=(fontFace, 36, "normal"))


def play(player1: dict[str, str], player2: dict[str, str], playerSet: bool = False, ballSpeedSet: bool = True, ballSpeed: int = 5, maxPoints: int = 3, width: int = 800, height: int = 600, bgcolor: str = "black"):
    game_over = False
    winner = None

    game_rules = {
        "max_points": maxPoints,
        "ball_speed": ballSpeed
    }

    game = Pong(width, height, bgcolor, ballSpeedSet,
                ballSpeed, playerSet, player1.get("name", "Player 1"), player2.get("name", "Player 2"), player1.get("color", "red"), player2.get("color", "blue"))

    game.setKeyboardBindings()

    while not game_over and winner is None:
        try:
            game.screen.update()
            game.moveBall()
            game.goingOutOfScreen()
            game.collisionWithScreen()
            game.collisionWithPaddles()
        except turtle.Terminator:
            print("Game stopped.", game)
            if game.getWinner() is None:
                print("No one wins.")
            else:
                print((game.player1 if game.getWinner ==
                      game.player1 else game.player2) + " wins.")
            exit(0)
        except _tkinter.TclError:
            print("Canvas error due to abrupt exit.")
            exit(0)

        # Check for game over conditions
        if game.points[game.player1] == game_rules["max_points"]:
            game_over = True
            winner = game.player1
        elif game.points[game.player2] == game_rules["max_points"]:
            game_over = True
            winner = game.player2

    # game ended
    game.displayGameOverScreen()

    turtle.done()
    print("Game Over!", game)
    print(f"{winner} wins!")


if __name__ == '__main__':
    player1 = {
        "name": "Player 1",  # change this
        # color name or rgb(r, g, b) values eg. rgb(255, 255, 255) or white
        "color": "red"
    }
    player2 = {
        "name": "Player 2",  # change this
        # color name or rgb(r, g, b) values eg. rgb(255, 255, 255) or white
        "color": "blue"
    }
    play(player1, player2, playerSet=False, ballSpeedSet=True, ballSpeed=5, maxPoints=3,
         width=800, height=600, bgcolor="black")
