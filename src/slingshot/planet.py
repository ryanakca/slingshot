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

import pygame
import math
from random import randint

from math import sqrt
from slingshot.settings import *
from slingshot.general import *

class Planet(pygame.sprite.Sprite):

	def __init__(self, planets, background, n=None, radius=None, mass=None, pos=None):
		pygame.sprite.Sprite.__init__(self)

		if n == None and planets != None:
			unique = False
			while not unique:
				unique = True
				self.n = randint(1, 8)
				for p in planets:
					if self.n == p.get_n():
						unique = False
		else:
			self.n = n

		filename = "data/planet_%d.png" %(self.n)
		self.orig, self.rect = load_image(filename, (0,0,0))
		self.image = self.orig

		if radius == None or mass == None or pos == None:
			positioned = False
			while not positioned:
				m = randint(0, (512-8)**2)
				self.mass = 8 + sqrt(m)
				self.mass = randint(8,512)
				self.r = self.mass**(1.0/3.0) * 12.5
				self.pos = (randint(Settings.PLANET_SHIP_DISTANCE + round(self.r), 800 - Settings.PLANET_SHIP_DISTANCE - round(self.r)), randint(Settings.PLANET_EDGE_DISTANCE + round(self.r), 600 - Settings.PLANET_EDGE_DISTANCE - round(self.r)))
				positioned = True
				for p in planets:
					d = math.sqrt((self.pos[0] - p.get_pos()[0])**2 + (self.pos[1] - p.get_pos()[1])**2)
					if d < (self.r + p.get_radius()) * 1.5 + 0.1 * (self.mass + p.get_mass()):
						positioned = False
		else:
			self.mass = mass
			self.r = radius
			self.pos = pos

		s = int(round(2 * self.r / 0.96))
		self.orig = pygame.transform.scale(self.image, (s, s))

		self.image = self.orig

		self.rect = self.orig.get_rect()
		self.rect.center = self.pos
		tmp = pygame.Surface(background.get_size())
		tmp.blit(background, (0,0))
		rect = tmp.blit(self.orig, self.rect.topleft)
		self.fade_image = pygame.Surface(self.orig.get_size())
		self.fade_image.blit(tmp, (0,0), rect)
		self.fade_image.set_alpha(255)
		self.fade_image.convert()

	def get_n(self):
		return self.n

	def get_radius(self):
		return self.r

	def get_mass(self):
		return self.mass

	def get_pos(self):
		return self.pos

	def fade(self, f):
		self.image = self.fade_image
		self.image.set_alpha(255 - round(f * 2.55))
#	def fade(self):
#		self.image = self.fade_image
#		self.image.blit(self.orig, (0,0))
#		for i in range(1, f):
#			r = round(self.r / 10)
#			pygame.draw.circle(self.image, (0,0,0,0), (randint(r, round(2 * self.r) - r), randint(r, round(2 * self.r) - r)), r)
#			for j in range(0, self.r):
#				self.image.set_at((randint(0, round(self.r * 2)), randint(0, round(self.r * 2))), (0,0,0,0))
