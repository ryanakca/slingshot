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

import pygame
from random import randint

import math
from slingshot.settings import *
from slingshot.general import *

class Player(pygame.sprite.Sprite):

	def __init__(self, n):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		self.player = n
		self.init()
		self.score = 0

	def init(self, y_coord = None):
		self.power = 100
		self.shot = False
		self.attempts = 0
		self.e = 0
		self.exp, self.rect = load_image("explosion.png", (0,0,0))

		if self.player == 1:
			self.angle = 90
			self.orig, self.rect = load_image("red_ship.png", (0,0,0))
			self.color = (209,170,133)
			self.rect = pygame.Rect(0,0,40,33)
			if y_coord == None:
				self.rect.midleft = (20,randint(100,500))
			else:
				self.rect.midleft = (20,y_coord)
			self.d = self.rect.right - self.rect.centerx + 2
			self.image = self.orig.subsurface(0, 0, 40, 33)
		elif self.player == 2:
			self.angle = 270
			self.orig, self.rect = load_image("blue_ship.png", (0,0,0))
			self.color = (132,152,192)
			self.rect = pygame.Rect(0,0,40,33)
			if y_coord == None:
				self.rect.midright = (780,randint(100,500))
			else:
				self.rect.midright = (780,y_coord)
			self.d = self.rect.centerx - self.rect.left + 3
			self.image = self.orig.subsurface(0, 0, 40, 33)
		else:
			self.orig = None

		self.rel_rot = 0.01

		if Settings.FIXED_POWER:
			self.power = Settings.POWER

		if Settings.FIXED_POWER:
			self.power = Settings.POWER

	def reset_score(self):
		self.score = 0

	def add_score(self, score):
		self.score = self.score + score

	def get_color(self):
		return self.color

	def change_angle(self, a):
		self.angle += a
		self.rel_rot += a
		if self.angle >= 360:
			self.angle -= 360
		if self.angle < 0:
			self.angle += 360
		if self.rel_rot >= 360:
			self.rel_rot -= 360
		if self.rel_rot < 0:
			self.rel_rot += 360
#		if Settings.ROTATE:
#			center = self.rect.center
#			self.image = pygame.transform.rotate(self.orig, -self.rel_rot)
#			self.image = self.image.convert_alpha()
#			self.rect = self.image.get_rect(center = center)

		center = self.rect.center
		#print "center0: (%d,%d)" %(self.rect.center[0], self.rect.center[1])

		img1 = round((self.rel_rot + 22.5) / 45 - 0.49) % 8
		img2 = round(self.rel_rot / 45 - 0.49) % 8
		if img1 == img2 or img1 == -img2:
			img2 = (img2 + 1) % 8
			f = (self.rel_rot - img1 * 45.0) / 45.0
		else:
			f = ((img2 + 1) * 45.0 - self.rel_rot) / 45.0

		rect1 = pygame.Rect(img1 * 40, 0, 40, 33)
		rect2 = pygame.Rect(img2 * 40, 0, 40, 33)
		image1 = self.orig.subsurface(rect1)
		image2 = self.orig.subsurface(rect2)
		image1 = image1.convert_alpha()
		image2 = image2.convert_alpha()

		tmp = pygame.Surface((40, 33))
		tmp = tmp.convert_alpha()
		tmp.blit(image2, (0,0))
		tmp = tmp.convert()
		tmp.set_alpha(round(255.0 * f))
		tmp.set_colorkey((0,0,0))
		tmp = tmp.convert_alpha()

		image1.blit(tmp,(0,0))

#		self.image = pygame.transform.rotate(image1, -self.rel_rot)
		self.image = pygame.transform.rotozoom(image1, -self.rel_rot, 1.0)
		self.rect = self.image.get_rect()
		#print "center1: (%d,%d)" %(self.rect.center[0], self.rect.center[1])
		self.rect.center = center
		#print "center2: (%d,%d)" %(self.rect.center[0], self.rect.center[1])


	def change_power(self, p):
		if not Settings.FIXED_POWER:
			self.power += p
			if self.power < 0:
				self.power = 0
			if self.power > Settings.MAXPOWER:
				self.power = Settings.MAXPOWER

	def get_angle(self):
		return self.angle

	def get_power(self):
		return self.power

	def get_launchpoint(self):
		if Settings.ROTATE:
			return (self.rect.center[0] + self.d * math.sin(math.radians(self.angle)), self.rect.center[1] - self.d * math.cos(math.radians(self.angle)))
		else:
			if self.player == 1:
				return (self.rect.midright[0] + 1, self.rect.midright[1])
			if self.player == 2:
				return (self.rect.midleft[0] - 1, self.rect.midleft[1])

	def get_rect_y_coord(self):
		if self.player == 1:
			return self.rect.midright[1]
		if self.player == 2:
			return self.rect.midleft[1]

	def draw_info(self, screen):
		txt = Settings.font.render("Angle: %3.2f" %(self.angle), 1, (255,255,255))
		rect = txt.get_rect()
		rect.topleft = (290, 5)
		screen.blit(txt, rect.topleft)

		txt = Settings.font.render("Power: %3.1f" %(self.power), 1, (255,255,255))
		rect = txt.get_rect()
		rect.topleft = (403, 5)
		screen.blit(txt, rect.topleft)

	def draw_status(self, screen):
		if self.player == 1:
			txt = Settings.font.render("Player 1  --  %d" %(self.score), 1, self.color)
			rect = txt.get_rect()
			rect.topleft = (5,5)
		else:
			txt = Settings.font.render("%d  --  Player 2" %(self.score), 1, self.color)
			rect = txt.get_rect()
			rect.topright = (794,5)
		screen.blit(txt, rect.topleft)

	def update_explosion(self):
		self.e = self.e + 1
		s = self.e * (6 - self.e) * 100 / 9
		if s >= 0:
			self.image = pygame.transform.scale(self.exp, (s,s))
			pos = self.rect.center
			self.rect = self.image.get_rect()
			self.rect.center = pos

	def draw_line(self, screen):
		(sx,sy) = self.get_launchpoint()

		pygame.draw.aaline(screen, self.color, (sx,sy), (sx + self.power * math.sin(math.radians(self.angle)), sy - self.power * math.cos(math.radians(self.angle))))

	def draw(self, screen):
		center = self.rect.center

		img1 = round((self.rel_rot + 22.5) / 45 - 0.4999) % 8
		img2 = round(self.rel_rot / 45 - 0.4999) % 8
		if img1 == img2:
			img2 = (img2 + 1) % 8
			f = (self.rel_rot - img1 * 45.0) / 45.0
		else:
			f = ((img2 + 1) * 45.0 - self.rel_rot) / 45.0
#			if img2 == 7:
#				f = f - 8.0

		print
		print img1
		print img2
		print f

		rect1 = pygame.Rect(img1 * 40, 0, 40, 33)
		rect2 = pygame.Rect(img2 * 40, 0, 40, 33)
		image1 = self.orig.subsurface(rect1)
		image2 = self.orig.subsurface(rect2)
#		image1.set_alpha(round(255.0 * (1.0 - f)))
		image1 = image1.convert_alpha()
		image2 = image2.convert_alpha()

		tmp = pygame.Surface((40, 33))
		tmp = tmp.convert_alpha()
		tmp.blit(image1, (0,0))
		tmp = tmp.convert()
		tmp.set_alpha(round(255.0 * (1.0 - f)))
		tmp.set_colorkey((0,0,0))
		tmp = tmp.convert_alpha()

		image2.blit(tmp,(0,0))

		self.image = pygame.transform.rotate(image2, self.rel_rot)
		self.rect = image.get_rect(center = center)

	def hit(self, pos):
		if not self.rect.collidepoint(pos):
			return False

		x = int(round(pos[0] - self.rect.topleft[0]))
		y = int(round(pos[1] - self.rect.topleft[1]))
		if x <= 1 or y <= 1:
			return False
		x = x - 1
		y = y - 1
		if not self.image.get_at((x,y)) == (0,0,0,0):
			self.shot = True
			return True
		else:
			return False

class Dummy(Player):

	def __init__(self):
		Player.__init__(self, 0)

	def draw_line(self, screen):
		pass

	def change_angle(self, a):
		pass

	def change_power(self, p):
		pass

	def draw_info(self, screen):
		pass
