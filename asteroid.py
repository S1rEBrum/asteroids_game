##################################################
# FILE : asteroid.py
# EXERCISE : intro2cs2 ex10 2021
# DESCRIPTION : File with characteristics of asteroids.
##################################################


from math import *


class Asteroid:
    # Given constants:
    SIZE = 3
    CONST = 10
    NORMAL = -5

    def __init__(self, x_coord, y_coord, x_speed, y_speed):
        """
        :param x_coord: x axis coordinate
        :param y_coord: y axis coordinate
        :param x_speed: speed at x axis
        :param y_speed: speed at y axis
        """
        self.__x_coord = x_coord
        self.__y_coord = y_coord
        self.__x_speed = x_speed
        self.__y_speed = y_speed
        # default value for size and radius calculated by given formula
        self.__size = self.SIZE
        self.__radius = self.__size * self.CONST + self.NORMAL

    # Getters and setters for asteroid characteristics:
    def get_location(self):
        return self.__x_coord, self.__y_coord

    def get_speed(self):
        return self.__x_speed, self.__y_speed

    def get_size(self):
        return self.__size

    def get_radius(self):
        """
        :return: radius of asteroid from default expression
        """
        return self.__radius

    def set_location(self, x, y):
        """
        :param x: new x coordinate
        :param y: new y coordinate
        :return: renews x and y for class Asteroid
        """
        self.__x_coord, self.__y_coord = x, y

    def set_speed(self, x, y):
        """
        :param x: new speed for x axis
        :param y: new speed for y axis
        :return: renews speed for x and y axis in Asteroid class
        """
        self.__x_speed, self.__y_speed = x, y

    def set_size(self, size):
        """
        :return: renews size for class Asteroid
        """
        self.__size = size - 1

    def has_intersection(self, obj):
        """
        :param obj: asteroid, ship, torpedo
        :return: returns True if there is intersection of object
        with asteroid
        """
        x_obj, y_obj = obj.get_location()
        x_asteroid, y_asteroid = self.get_location()
        dst = sqrt(pow(x_obj - x_asteroid, 2) + pow(y_obj - y_asteroid, 2))
        if dst <= self.get_radius() + obj.get_radius():
            return True
        return False
