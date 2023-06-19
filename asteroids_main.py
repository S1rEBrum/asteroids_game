#######################################################################################
# FILE : asteroids_main.py
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION : Main game file which includes all imported data of game objects from:
# screen.py, torpedo.py, ship.py and asteroid.py. GameRunner class runs asteroids
# game with help of builtin python modules and new methods of the class for the game.
# Game is shown on the screen and it is interactive, user can change direction and
# speed of spaceship, shoot with up to 10 torpedoes in one time, get score and amount
# of lives remained on the screen. Purpose of the game: collapse all asteroids 5 until
# they completely disappear and to save at least one life till the end. If no life or
# asteroid is left or user wrote q - than game is over. Each important change is
# followed by relevant message.
########################################################################################


from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from random import *
from math import *
import sys

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    # Given initial constants:
    INIT_X_SPEED = INIT_Y_SPEED = INIT_DIRECTION = INIT_SCORE = 0
    MIN_AST_SPEED = 1
    MAX_AST_SPEED = 4
    COLL_TITLE = "COLLISION!!!"
    COLL_MESSAGE = "You were hit by an asteroid!"
    END = "GAME OVER!"
    WIN = "YOU WON!!!"
    LIVES_ENDED = "There are no lives left!"
    NO_AST_LEFT = "You won! There are no asteroids left!"
    USER_MSG = "You decided to quit... Goodbye!!!"
    SCORE = {1: 100, 2: 50, 3: 20}
    TORPEDOES_AMOUNT = 10

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        self.__ship = Ship(self.generate_randomly()[0], self.generate_randomly()[1],
                           self.INIT_X_SPEED, self.INIT_Y_SPEED, self.INIT_DIRECTION)

        self.__asteroids = self.add_asteroids(asteroids_amount)    # adding asteroids
        self.__torpedoes = []
        self.__score = self.INIT_SCORE

    def generate_randomly(self):
        """
        :return: Random coordinates on the screen.
        """
        x_random = randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
        y_random = randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
        return x_random, y_random

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        # check if the game has ended
        self.end()
        # move all objects
        self.move()
        # take the user input on the keyboard
        self.user_input()
        # check if the ship collided into the asteroid
        self.collision_asteroid_ship()
        # check if the torpedo collided into the asteroid
        self.collision_asteroid_torpedo()
        # reduce torpedoes lifetime
        self.torpedo_lifetime()
        # draw all the objects on the screen due to the changes
        self.draw_object()

    def user_input(self):
        if self.__screen.is_left_pressed():
            self.__ship.set_direction("l")
        if self.__screen.is_right_pressed():
            self.__ship.set_direction("r")
        if self.__screen.is_up_pressed():
            self.__ship.set_speed()
        if self.__screen.is_space_pressed():
            # If less than 10 torpedoes on the screen:
            if len(self.__torpedoes) < self.TORPEDOES_AMOUNT:
                self.add_torpedo()

    def draw_object(self):
        """
        Calls for draw_object method relevant to each object
        from class Screen
        :return: draws objects on the screen
        """
        # draw ship
        self.__screen.draw_ship(self.__ship.get_location()[0],
                                self.__ship.get_location()[1],
                                self.__ship.get_direction())
        # draw all asteroids
        for asteroid in self.__asteroids:
            self.__screen.draw_asteroid(asteroid,
                                        asteroid.get_location()[0],
                                        asteroid.get_location()[1])
        # draw all torpedoes
        for torpedo in self.__torpedoes:
            self.__screen.draw_torpedo(torpedo,
                                       torpedo.get_location()[0],
                                       torpedo.get_location()[1],
                                       self.__ship.get_in_radians())  # torpedoes appear exactly at ship`s location

    def add_asteroids(self, amount):
        """
        :param amount: amount of drawn asteroids, default = 5
        :return: list of details about asteroids
        """
        ast_lst = []
        for i in range(amount):
            # placing asteroids randomly on the screen with random speed
            asteroid = Asteroid(self.generate_randomly()[0], self.generate_randomly()[1],
                                randint(self.MIN_AST_SPEED, self.MAX_AST_SPEED),
                                randint(self.MIN_AST_SPEED, self.MAX_AST_SPEED))
            # list of asteroids for intersection test
            ast_lst.append(asteroid)
            self.__screen.register_asteroid(asteroid, asteroid.get_size())
        return ast_lst

    def end(self):
        """
        Game is over if no lives of ship left or all asteroids are collapsed
        or user wrote q for exit.
        """
        if self.__ship.get_lives() == 0:  # All 3 lives have been used
            self.__screen.show_message(self.END, self.LIVES_ENDED)
            self.__screen.end_game()    # Screen class method
            sys.exit()
        if len(self.__asteroids) == 0:  # All asteroids are collapsed
            self.__screen.show_message(self.WIN, self.NO_AST_LEFT)
            self.__screen.end_game()
            sys.exit()
        if self.__screen.should_end():  # User entered q (Screen class method)
            self.__screen.show_message(self.END, self.USER_MSG)
            self.__screen.end_game()
            sys.exit()

    def move(self):
        """
        Moves space objects with unified formula
        :return: new coordinates of object
        """
        objects = self.__asteroids + self.__torpedoes + [self.__ship]
        for obj in objects:
            delta = self.__screen_max_x - self.__screen_min_x
            old_x, old_y = obj.get_location()
            x_speed, y_speed = obj.get_speed()
            new_x = (old_x + x_speed - self.__screen_min_x) % delta\
                + self.__screen_min_x
            new_y = (old_y + y_speed - self.__screen_min_y) % delta\
                + self.__screen_min_y
            obj.set_location(new_x, new_y)

    def collision_asteroid_ship(self):
        """
        Checks if asteroid and ship have intersection and if True
        sends message and deletes visual symbol of life from screen
        with show_message and remove_life functions from class Screen.
        """
        for asteroid in self.__asteroids:
            if asteroid.has_intersection(self.__ship):
                self.__screen.show_message(self.COLL_TITLE, self.COLL_MESSAGE)  # Screen class method
                if self.__ship.get_lives() > 0:  # if there are lives left
                    self.__ship.remove_life()
                    self.__screen.remove_life()
                # removing asteroid if intersection with torpedo
                self.__screen.unregister_asteroid(asteroid)
                self.__asteroids.remove(asteroid)

    def add_torpedo(self):
        """
        Adding torpedo to the screen and registering them to torpedoes list.
        """
        # torpedo appears at the location of the ship
        x_location, y_location = self.__ship.get_location()
        x_speed, y_speed = self.__ship.get_speed()
        direction = self.__ship.get_direction()
        torpedo = Torpedo(x_location, y_location, x_speed, y_speed, direction)
        self.__torpedoes.append(torpedo)
        self.__screen.register_torpedo(torpedo)

    def torpedo_lifetime(self):
        """
        Removes torpedoes from screen after default amount of 200 loops is over.
        """
        for torpedo in self.__torpedoes:
            torpedo.set_lifetime()
            if torpedo.get_lifetime() == 0:
                self.__screen.unregister_torpedo(torpedo)
                self.__torpedoes.remove(torpedo)

    def collision_asteroid_torpedo(self):
        """
        Checks with has_intersection method from Asteroid class if there
        is intersection between torpedo and asteroid, if yes, than score
        is changed with method count_score and torpedo is removed. If
        asteroid has bigger size than 1, than it is separated. Otherwise
        it is deleted from screen and from count.
        :return:
        """
        for asteroid in self.__asteroids:
            for torpedo in self.__torpedoes:
                if asteroid.has_intersection(torpedo):
                    self.count_score(asteroid)
                    self.__screen.unregister_torpedo(torpedo)
                    self.__torpedoes.remove(torpedo)
                    if asteroid.get_size() == 1:  # asteroid has minimal size
                        self.__screen.unregister_asteroid(asteroid)
                        self.__asteroids.remove(asteroid)
                    else:  # asteroid is separated
                        self.asteroid_separation(asteroid, torpedo)

    def asteroid_new_speed(self, asteroid, torpedo):
        """
        Setting new speed for asteroid with given expression.
        :param asteroid: intersection with torpedo is True
        :param torpedo: intersection with asteroid is True
        :return: new asteroid speed on x and y axis after intersection
        """
        x_asteroid, y_asteroid = asteroid.get_speed()
        x_torpedo, y_torpedo = torpedo.get_speed()
        x_new = (x_torpedo + x_asteroid) / sqrt(pow(x_asteroid, 2) + pow(y_asteroid, 2))
        y_new = (y_torpedo + y_asteroid) / sqrt(pow(x_asteroid, 2) + pow(y_asteroid, 2))
        return x_new, y_new

    def asteroid_separation(self, asteroid, torpedo):
        """
         Asteroid is separated into two and both of new asteroids
         have renewed size, direction and speed. Old asteroid is removed.
         :param asteroid: intersection with torpedo is True
         :param torpedo: intersection with asteroid is True
         """
        size = asteroid.get_size()
        x_location, y_location = asteroid.get_location()
        x_speed, y_speed = self.asteroid_new_speed(asteroid, torpedo)

        # New two asteroids are objects from Asteroid class
        smaller_asteroid1 = Asteroid(x_location, y_location, x_speed, y_speed)
        smaller_asteroid1.set_size(size)

        smaller_asteroid2 = Asteroid(x_location, y_location, -x_speed, -y_speed)
        smaller_asteroid2.set_size(size)

        # Old asteroid is removed from screen and list
        self.__screen.unregister_asteroid(asteroid)
        self.__asteroids.remove(asteroid)

        # New asteroids are registered in the list and added to the screen.
        self.__asteroids.append(smaller_asteroid1)
        self.__asteroids.append(smaller_asteroid2)
        self.__screen.register_asteroid(smaller_asteroid1, smaller_asteroid1.get_size())
        self.__screen.register_asteroid(smaller_asteroid2, smaller_asteroid2.get_size())

    def count_score(self, asteroid):
        """
        Identifying size of asteroid and usage of SCORE dictionary for
        score updates.
        :param asteroid: asteroid with torpedo intersection
        :return: updating score, changing value on screen
        """
        for key in self.SCORE:
            if key == asteroid.get_size():
                # using dictionary to reduce runtime
                self.__score += self.SCORE[key]
        self.__screen.set_score(self.__score)


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
