##################################################
# FILE : torpedo.py
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION : File with characteristics of torpedo.
##################################################


from math import *


class Torpedo:
    # Given constants:
    RADIUS = 4
    LIFETIME = 200
    ACCELERATION = 2

    def __init__(self, x_coord, y_coord, x_speed, y_speed, direction):
        """
        :param x_coord: x axis coordinate
        :param y_coord: y axis coordinate
        :param x_speed: speed at x axis
        :param y_speed: speed at y axis
        :param direction: direction of the torpedo in degrees
        """
        self.__x_coord = x_coord
        self.__y_coord = y_coord
        self.__direction = direction
        self.__x_speed = x_speed + self.ACCELERATION * cos(radians(self.__direction))
        self.__y_speed = y_speed + self.ACCELERATION * sin(radians(self.__direction))
        # default values for radius and lifetime
        self.__radius = self.RADIUS
        self.__lifetime = self.LIFETIME

    # Getters and setters of torpedo characteristics:
    def get_location(self):
        return self.__x_coord, self.__y_coord

    def get_speed(self):
        return self.__x_speed, self.__y_speed

    def get_lifetime(self):
        return self.__lifetime

    def get_radius(self):
        return self.__radius

    def set_location(self, x, y):
        """
        :param x: ship x axis coordinate
        :param y: ship y axis coordinate
        :return: sets x and y coordinates as of ship
        """
        self.__x_coord, self.__y_coord = x, y

    def set_lifetime(self):
        """
        Counts left lifetime for torpedo. Maximum default value
        is 200.
        """
        self.__lifetime -= 1
