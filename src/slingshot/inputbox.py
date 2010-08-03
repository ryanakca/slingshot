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

import pygame, string

from pygame.locals import *
from slingshot.settings import *


class Inputbox:

	def __init__(self, screen, question):
		self.screen = screen
		self.question = question
		self.new_str = []
		self.input_box(question + ": " + string.join(self.new_str,""))

	def input_box(self, msg):
		pygame.draw.rect(self.screen, (0,0,0),
				 ((self.screen.get_width() / 2) - 200,
				  (self.screen.get_height() / 2) - 20,
				  400,40), 0)
		pygame.draw.rect(self.screen, (255,255,255),
				 ((self.screen.get_width() / 2) - 204,
				  (self.screen.get_height() / 2) - 24,
				  408,48), 1)

		if len(msg) != 0:
			self.screen.blit(Settings.menu_font.render(msg, 1, (255,255,255)),
				    ((self.screen.get_width() / 2) - 200, (self.screen.get_height() / 2) - 12))
			pygame.display.flip()

	def ask(self):
		while 1:
			key = self.get_key()
			if key == K_BACKSPACE:
				self.new_str = self.new_str[0:-1]
			elif key == K_RETURN:
				break
			elif key == K_ESCAPE:
				return False
			elif key <= 127 and len(self.new_str) < 19:
				self.new_str.append(chr(key))
			self.input_box(self.question + ": " + string.join(self.new_str,""))
		return string.join(self.new_str,"")

	def get_key(self):
		while 1:
			event = pygame.event.poll()
			if event.type == KEYDOWN:
				return event.key
