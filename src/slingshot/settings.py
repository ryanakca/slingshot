#    This file is part of Slingshot.
#
# Slingshot is a two-dimensional strategy game where two players attempt to shoot one
# another through a section of space populated by planets.  The main feature of the
# game is that the shots, once fired, are affected by the gravity of the planets.

# Slingshot is Copyright 2007 Jonathan Musther and Bart Mak. It is released under the
# terms of the GNU General Public License version 2, or later if applicable.

# Slingshot is free software; you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation; either
# version 2 of the License, or any later version.

# Slingshot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with Slingshot;
# if not, write to
# the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

# Copyright (C) 2009 Marcus Dreier <m-rei@gmx.net>
# Copyright (C) 2010 Ryan Kavanagh <ryanakca@kubuntu.org>

import os.path

class Settings:

        VERSION = '0.9 (unreleased)'

	g = 120 # gravity
	MAXPOWER = 350
	PLANET_SHIP_DISTANCE = 75 # this is actually the distance towards the edge left and right
	PLANET_EDGE_DISTANCE = 50 # upper and lower edge

	PARTICLE_5_MINSPEED = 100
	PARTICLE_5_MAXSPEED = 200 # 200: easy, 300: wild
	PARTICLE_10_MINSPEED = 150
	PARTICLE_10_MAXSPEED = 250 # 250 easy, 400-500 wild
	n_PARTICLES_5 = 20  # number of small particles originating from a big one
	n_PARTICLES_10 = 30 # number of big particles originating from explosion
		# if both are too high, the game stalls on impact

	ROTATE = True
	BOUNCE = False
	FIXED_POWER = False
	PARTICLES = True
	INVISIBLE = False
	RANDOM = False
	POWER = 200

	MAX_FLIGHT = 750

	MAX_PLANETS = 4

	HITSCORE = 1500
	SELFHIT = 2000
	QUICKSCORE1 = 500
	QUICKSCORE2 = 200
	QUICKSCORE3 = 100

	PENALTY_FACTOR = 5

	FPS = 30
	KEY_REPEAT = 30 # time between repeating key events, keep a little lower than 1000 / FPS
	KEY_DELAY = 250

	MENU_FONT_SIZE = 26
	MENU_LINEFEED = 36

	MAX_ROUNDS = 0

        DATA_PATH = os.path.join(os.path.dirname(__file__), 'data/')

        FULLSCREEN = False
