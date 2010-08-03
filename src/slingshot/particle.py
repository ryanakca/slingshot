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

from slingshot.settings import *
from slingshot.general import *
import pygame
import math
from math import sqrt
from random import randint

class Particle(pygame.sprite.Sprite):

	def __init__(self, pos = (0.0, 0.0), size = 10):
		pygame.sprite.Sprite.__init__(self)
		if size == 5:
			self.image = Settings.particle_image5
		else:
			self.image = Settings.particle_image10
		self.rect = self.image.get_rect()
#		self.image, self.rect = load_image("explosion-10.png", (0,0,0))
		self.pos = pos
		self.impact_pos = pos
		self.size = size
		angle = randint(0, 359)
		if size == 5:
			speed = randint(Settings.PARTICLE_5_MINSPEED,Settings.PARTICLE_5_MAXSPEED)
		else:
			speed = randint(Settings.PARTICLE_10_MINSPEED,Settings.PARTICLE_10_MAXSPEED)
		self.v = (0.1 * speed * math.sin(angle), -0.1 * speed * math.cos(angle))
		self.flight = Settings.MAX_FLIGHT

	def max_flight(self):
		if self.flight < 0:
			return True
		else:
			return False

	def update(self, planets):
		self.flight = self.flight - 1

		self.last_pos = self.pos

		for p in planets:
			p_pos = p.get_pos()
			mass = p.get_mass()
			d = (self.pos[0] - p_pos[0])**2 + (self.pos[1] - p_pos[1])**2
			a = (Settings.g * mass * (self.pos[0] - p_pos[0]) / (d * math.sqrt(d)), Settings.g * mass * (self.pos[1] - p_pos[1]) / (d * math.sqrt(d)))
			self.v = (self.v[0] - a[0], self.v[1] - a[1])

		self.pos = (self.pos[0] + self.v[0], self.pos[1] + self.v[1])

		if not self.in_range():
			return 0

		for p in planets:
			p_pos = p.get_pos()
			r = p.get_radius()
			d = (self.pos[0] - p_pos[0])**2 + (self.pos[1] - p_pos[1])**2
			if d <= (r)**2:
				self.impact_pos = get_intersect(p_pos, r, self.last_pos, self.pos)
				self.pos = self.impact_pos
				return 0

		if Settings.BOUNCE:
			if self.pos[0] > 799:
				d = self.pos[0] - self.last_pos[0]
				self.pos = (799, self.last_pos[1] + (self.pos[1] - self.last_pos[1]) * (799 - self.last_pos[0]) / d)
				self.v = (-self.v[0], self.v[1])
			if self.pos[0] < 0:
				d = self.last_pos[0] - self.pos[0]
				self.pos = (0,self.last_pos[1] +  (self.pos[1] - self.last_pos[1]) * self.last_pos[0] / d)
				self.v = (-self.v[0], self.v[1])
			if self.pos[1] > 599:
				d = self.pos[1] - self.last_pos[1]
				self.pos = (self.last_pos[0] + (self.pos[0] - self.last_pos[0]) * (599 - self.last_pos[1]) / d, 599)
				self.v = (self.v[0], -self.v[1])
			if self.pos[1] < 0:
				d = self.last_pos[1] - self.pos[1]
				self.pos = (self.last_pos[0] + (self.pos[0] - self.last_pos[0]) * self.last_pos[1] / d, 0)
				self.v = (self.v[0], -self.v[1])
#				print self.pos
#				print self.last_pos

		self.rect.center = (round(self.pos[0]), round(self.pos[1]))
		return 1

	def in_range(self):
		if pygame.Rect(-800, -600, 2400, 1800).collidepoint(self.pos):
			return True
		else:
			return False

	def visible(self):
		if pygame.Rect(0, 0, 800, 600).collidepoint(self.pos):
			return True
		else:
			return False

	def get_pos(self):
		return self.pos

	def get_impact_pos(self):
		return self.impact_pos

	def get_size(self):
		return self.size

class Missile(Particle):

	def __init__(self, trail_screen):
		Particle.__init__(self) #call Sprite intializer
		self.image, self.rect = load_image("data/shot.png", (0,0,0))
		self.rect = self.image.get_rect()
		self.trail_screen = trail_screen
		self.last_pos = (0.0, 0.0)

	def launch(self, player):
		self.flight = Settings.MAX_FLIGHT
		self.pos = player.get_launchpoint()
		speed = player.get_power()
		angle = math.radians(player.get_angle())
		self.v = (0.1 * speed * math.sin(angle), -0.1 * speed * math.cos(angle))
		self.trail_color = player.get_color()

		self.score = -Settings.PENALTY_FACTOR * speed

	def update_players(self, players):
		result = 1

		for i in xrange(10):
			pos = (self.last_pos[0] + i * 0.1 * self.v[0], self.last_pos[1] + i * 0.1 * self.v[1])
			if players[1].hit(pos):
				result = 0
			if players[2].hit(pos):
				result = 0
			if result == 0:
				self.impact_pos = pos
				self.pos = pos
				break
		return result

	def draw_status(self, screen):
		txt = Settings.font.render("Power penalty: %d" %(-self.score), 1, (255,255,255))
		rect = txt.get_rect()
		rect.midtop = (399, 5)
		screen.blit(txt, rect.topleft)
		if self.flight >= 0:
			txt = Settings.font.render("Timeout in %d" %(self.flight), 1,(255,255,255))
		else:
			txt = Settings.font.render("Shot timed out...", 1, (255,255,255))
		rect = txt.get_rect()
		rect.midbottom = (399, 594)
		screen.blit(txt, rect.topleft)


	def update(self, planets, players):
		result = Particle.update(self, planets)
		result = result * self.update_players(players)
		pygame.draw.aaline(self.trail_screen, self.trail_color, self.last_pos, self.pos)
		return result

	def get_image(self):
		return self.image

	def get_score(self):
		return self.score
