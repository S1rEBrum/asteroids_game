##################################################
# FILE : ship.py
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION : File with characteristics of ship.
##################################################


from math import *


class Ship:
    # Given constants:
    LIVES = 3
    RADIUS = 1
    DELTA_DIR = 7

    def __init__(self, x_coord, y_coord, x_speed, y_speed, direction):
        """
        :param x_coord: x axis coordinate
        :param y_coord: y axis coordinate
        :param x_speed: speed at x axis
        :param y_speed: speed at y axis
        :param direction: direction of the ship in degrees
        """
        self.__x_coord = x_coord
        self.__y_coord = y_coord
        self.__x_speed = x_speed
        self.__y_speed = y_speed
        self.__direction = direction
        # default values for lives and radius
        self.__lives = self.LIVES
        self.__radius = self.RADIUS

    # Getter and setters for ship characteristics.
    def get_location(self):
        return self.__x_coord, self.__y_coord

    def get_speed(self):
        return self.__x_speed, self.__y_speed

    def get_direction(self):
        return self.__direction

    def get_in_radians(self):
        """
        Renews direction value in ship description.
        """
        return radians(self.__direction)

    def get_lives(self):
        """
        Gives lives for ship. Default value is 3.
        """
        return self.__lives

    def get_radius(self):
        """
        Returns radius of ship, when default value is 1.
        """
        return self.__radius

    def set_location(self, x, y):
        """
        :param x: new x axis coordinate
        :param y: new y axis coordinate
        :return: renews x and y axis coordinates for ship
        """
        self.__x_coord, self.__y_coord = x, y

    def set_speed(self):
        """
        :return: increase speed in x and y axis
        """
        self.__x_speed = self.__x_speed + cos(radians(self.__direction))
        self.__y_speed = self.__y_speed + sin(radians(self.__direction))

    def set_direction(self, side):
        """
        Increase in 7 degrees if left heading.
        Decrease of 7 degrees if right heading.
        """
        if side == "l":
            self.__direction += self.DELTA_DIR
        if side == "r":
            self.__direction -= self.DELTA_DIR

    def remove_life(self):
        """
        Decrease 1 life of the ship.
        """
        self.__lives -= 1
