#!/usr/bin/env python

###
# Conway's game of life for Unicorn Hat
# (C) 2014  Alex Crouzen
# Shared under the MIT permissive license.
###

import random
import time
import unicornhat as unicorn


class LifeCell:
    """
    Central class defining both the cells and the matrix of cells.
    """

    matrix = {}     # the matrix of cells

    def __init__(self, initial_x, initial_y, initial_state='alive'):
        """
        Create a new cell

        :param initial_x:
        :param initial_y:
        :param initial_state:
        """
        self.x = initial_x
        self.y = initial_y
        self.current_state = initial_state
        self.next_state = 'unknown'
        coordinate_tuple = (x, y)
        if coordinate_tuple not in LifeCell.matrix:
            LifeCell.matrix[coordinate_tuple] = self
        else:
            print "Cell already exists at %d,%d" % (x, y)

    @staticmethod
    def wipe_matrix():
        """
        Wipe the matrix
        """
        LifeCell.matrix = {}

    @staticmethod
    def matrix_value():
        """
        Calculate the current state of the matrix (== the sum of all 'alive' cells)
        :return: the 'value' of the matrix
        """
        count = 0
        for iter_cell in LifeCell.matrix.itervalues():
            if iter_cell.current_state == 'alive':
                count += 1
        return count

    @staticmethod
    def get_neighbour_surrent_state(x, y):
        """
        Get the 'state' of a neighbour
        :param x:
        :param y:
        :return: 1 if alive, 0 if not.
        """
        coordinate_tuple = (x, y)
        if coordinate_tuple in LifeCell.matrix:
            if LifeCell.matrix[coordinate_tuple].current_state == 'alive':
                return 1
        return 0

    @staticmethod
    def display_matrix(max_x, max_y, text=False, r=255, g=255, b=255):
        """
        Display the matrix, either on the unicorn or on the stdout
        :param max_x:
        :param max_y:
        :param text: If True, display on stdout instead of unicornhat. For debugging
        """
        if text:
            for x in range(max_x):
                for y in range(max_y):
                    coordinate_tuple = (x, y)
                    if LifeCell.matrix[coordinate_tuple].current_state == 'alive':
                        print '*',
                    else:
                        print '.',
                print
            print
        else:
            for x in range(max_x):
                for y in range(max_y):
                    coordinate_tuple = (x, y)
                    if LifeCell.matrix[coordinate_tuple].current_state == 'alive':
                        unicorn.set_pixel(x, y, r, g, b)
                    else:
                        unicorn.set_pixel(x, y, 0, 0, 0)
            unicorn.show()

    @staticmethod
    def progress_generation():
        """
        Step to the next generation
        """
        for iter_cell in LifeCell.matrix.itervalues():
            alive_neightbours = iter_cell.get_alive_neighbours()
            if iter_cell.current_state == 'alive':
                if alive_neightbours < 2:
                    iter_cell.next_state = 'dead'
                elif alive_neightbours > 3:
                    iter_cell.next_state = 'dead'
                else:
                    iter_cell.next_state = 'alive'
            else:
                if alive_neightbours == 3:
                    iter_cell.next_state = 'alive'
                else:
                    iter_cell.next_state = 'dead'
        for iter_cell in LifeCell.matrix.itervalues():
            iter_cell.progress_state()

    def get_alive_neighbours(self):
        """
        calculate the number of neighbours that are alive
        :return: the number of neighbors currently alive
        """
        alive_count = 0
        alive_count += LifeCell.get_neighbour_surrent_state(self.x-1, self.y-1)
        alive_count += LifeCell.get_neighbour_surrent_state(self.x, self.y-1)
        alive_count += LifeCell.get_neighbour_surrent_state(self.x+1, self.y-1)
        alive_count += LifeCell.get_neighbour_surrent_state(self.x-1, self.y)

        alive_count += LifeCell.get_neighbour_surrent_state(self.x+1, self.y)
        alive_count += LifeCell.get_neighbour_surrent_state(self.x-1, self.y+1)
        alive_count += LifeCell.get_neighbour_surrent_state(self.x, self.y+1)
        alive_count += LifeCell.get_neighbour_surrent_state(self.x+1, self.y+1)

        return alive_count

    def progress_state(self):
        """
        Progress to the next generation for one cell.
        """
        self.current_state = self.next_state
        self.next_state = 'unknown'


# Main program loop
if __name__ == "__main__":
    # set comfortable brightness
    unicorn.brightness(0.2)

    # unicorn hat size
    max_x = 7
    max_y = 7

    # Will forever show loops of 50 generations.
    while True:
        cells = []
        LifeCell.wipe_matrix()
        # create a random colour
        random_r = random.randint(0, 255)
        random_g = random.randint(0, 255)
        random_b = random.randint(0, 255)
        for x in range(max_x):
            for y in range(max_y):
                cell = LifeCell(x, y, random.choice(('alive', 'dead')))     # randomly populate the matrix
                cells.append(cell)

        for count in range(50):
            LifeCell.progress_generation()
            LifeCell.display_matrix(max_x, max_y, False, random_r, random_g, random_b)    # use the unicorn hat
            time.sleep(0.1)
            if LifeCell.matrix_value() == 0:
                break

