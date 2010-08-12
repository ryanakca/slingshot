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
from slingshot.settings import *
from slingshot.general import *

class Menu:

	def __init__(self, name, dim = True, copyright = False):
		self.reset()
		self.items = []
		self.name = name
		self.dim = dim
		self.count = 0
		self.inc = 15
                self.copyright = copyright

	def change_active(self, item, a):
		for i in xrange(0, self.items.__len__()):
			if self.items[i][0] == item:
				self.items[i] = (self.items[i][0], self.items[i][1], self.items[i][2], a)

	def add(self, item):
		self.items.append((item, 0, False, True))

	def addoption(self, item, v = False, a = True):
		self.items.append((item, 1, v, a))

	def up(self):
		self.selected = self.selected - 1
		if self.selected < 0:
			self.selected = self.items.__len__() - 1
		if self.items[self.selected][3] == False:
			self.up()

	def left(self):
		self.up()

	def down(self):
		self.selected = self.selected + 1
		if self.selected >= self.items.__len__():
			self.selected = 0
		if self.items[self.selected][3] == False:
			self.down()

	def right(self):
		self.down()

	def select(self):
		return self.items[selected][0]

	def reset(self):
		self.selected = 0
		self.choice = ""

	def get_width(self):
		#return 300
		return 350

	def get_height(self):
		#n = self.items.__len__()
		#return 44 * n + 100
		return 500

	def select(self):
		if self.items[self.selected][1]:
			self.items[self.selected] = (self.items[self.selected][0], self.items[self.selected][1], not self.items[self.selected][2], self.items[self.selected][3])
		self.choice = self.items[self.selected][0]

	def get_choice(self):
		c = self.choice
		self.choice = ""
		return c

	def draw(self):
		w = self.get_width()
		h = self.get_height()
		result = pygame.Surface((w, h))
		#result.fill((100,0,0))
		result.blit(Settings.menu_background, (0,0))
                if self.copyright:
                        for line, (x, y) in prep_text([
"Slingshot is:",
"    Copyright (C) 2007 Jonathan Musther <jmusther@gmail.com>",
"    Copyright (C) 2007 Bart Mak",
"    Copyright (C) 2009 Marcus Dreier <m-rei@gmx.net>",
"    Copyright (C) 2010 Ryan Kavanagh <ryanakca@kubuntu.org>",
"",
"Slingshot is free software; you can redistribute it and/or modify",
"it under the terms of the GNU General Public License as published by",
"the Free Software Foundation; either version 2 of the License, or",
"(at your option) any later version.",
"",
"Slingshot is distributed in the hope that it will be useful,",
"but WITHOUT ANY WARRANTY; without even the implied warranty of",
"MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the",
"GNU General Public License for more details.",
"",
"You should have received a copy of the GNU General Public License",
"along with Slingshot; if not, write to the Free Software",
"Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA",
"",
"http://github.com/ryanakca/slingshot"],
                                True, Settings.fineprint, 0, (10, 10, 10)):
                            # We want our text to start at 20px from the left
                            # side and 305 px from the top.
                            result.blit(line, (20, 305 + y))

		txt = Settings.menu_font.render(self.name, 1, (255,255,255))
		rect = txt.get_rect()
		rect.midtop = (w / 2, Settings.MENU_LINEFEED)
		result.blit(txt, rect.topleft)

		n = self.items.__len__()
		for i in xrange(0, n):
			if i == self.selected:
				color = (self.count,self.count,255)
			else:
				if self.items[i][3] == True:
					color = (0,0,255)
				else:
					color = (75,75,75)
			txt = Settings.menu_font.render(self.items[i][0], 1, color)
			if self.items[i][1] == 1:
				offset = 35
				result.blit(Settings.box, (25, 2.5 * Settings.MENU_LINEFEED + Settings.MENU_LINEFEED * i - 8))
				if self.items[i][2]:
					if self.items[i][3]:
						result.blit(Settings.tick, (25, 2.5 * Settings.MENU_LINEFEED + Settings.MENU_LINEFEED * i - 8))
					else:
						result.blit(Settings.tick_inactive, (25, 2.5 * Settings.MENU_LINEFEED + Settings.MENU_LINEFEED * i - 8))
			else:
				offset = 0
			result.blit(txt, (25 + offset,2.5 * Settings.MENU_LINEFEED + Settings.MENU_LINEFEED * i))

		pygame.draw.rect(result, (0,0,200), pygame.Rect(0, 0, w, h), 1)

		self.count += self.inc
		if self.count > 255 or self.count < 0:
			self.inc *= -1
			self.count += 2* self.inc

		return result

class Help(Menu):

	def __init__(self):
		Menu.__init__(self, "", False)
		self.img, rect = load_image("help.png", (0,0,0))
		self.choice = ""

	def select(self):
		self.choice = "Back"

	def draw(self):
		return self.img

	def up(self):
		pass

	def down(self):
		pass

class Welcome(Menu):

	def __init__(self):
		Menu.__init__(self, "")
                self.img = pygame.surface.Surface((600, 300), pygame.SRCALPHA)
		self.choice = ""
                # header font
                hfont = pygame.font.Font(get_data_path("FreeSansBold.ttf"), 40)
                header = prep_text(["Welcome to Slingshot!"], True, hfont,
                                 0, (255, 255, 255))[0]
                self.img.blit(header[0],
                              ((self.img.get_width() - header[1][0]) / 2, 0)
                             )
                # Instructions font
                ifont = pygame.font.Font(get_data_path("FreeSansBold.ttf"), 15)
                instructions = prep_text(
                    ["Press space to play or escape for the menu and help!"],
                    True, ifont, 0, (255, 255, 255))[0]
                self.img.blit(instructions[0],
                          ((self.img.get_width() - instructions[1][0]) / 2, 60)
                             )
                for line, (x, y) in prep_text([
"Slingshot is:",
"    Copyright (C) 2007 Jonathan Musther <jmusther@gmail.com>",
"    Copyright (C) 2007 Bart Mak",
"    Copyright (C) 2009 Marcus Dreier <m-rei@gmx.net>",
"    Copyright (C) 2010 Ryan Kavanagh <ryanakca@kubuntu.org>",
"",
"Slingshot is free software; you can redistribute it and/or modify",
"it under the terms of the GNU General Public License as published by",
"the Free Software Foundation; either version 2 of the License, or",
"(at your option) any later version."],
                                    True, Settings.font, 0, (150, 150, 150)):
                        # We want our text to start at 100px from the left side
                        # and 100 px from the top.
                        self.img.blit(line, (100, 110 + y))

	def select(self):
		self.choice = "Start"

	def draw(self):
		return self.img

	def up(self):
		pass

	def down(self):
		pass

class Numeric(Menu):

	def __init__(self, txt, init, step, mmax, mmin = 0, inf = "0"):
		Menu.__init__(self, txt)
		self.val = init
		self.step = step
		self.mmax = mmax
		self.mmin = mmin
		self.inf = inf
		self.choice = -1

	def up(self):
		self.val += self.step
		if self.val > self.mmax:
			self.val = self.mmax

	def down(self):
		self.val -= self.step
		if self.val < self.mmin:
			self.val = self.mmin

	def select(self):
		self.choice = self.val

	def get_choice(self):
		c = self.choice
		self.choice = -1
		return c

	def draw(self):
		w = self.get_width()
		h = self.get_height()
		result = pygame.Surface((w, h))

		result.blit(Settings.menu_background, (0,0))

		txt = Settings.menu_font.render(self.name, 1, (255,255,255))
		rect = txt.get_rect()
		rect.midtop = (w / 2, Settings.MENU_LINEFEED)
		result.blit(txt, rect.topleft)

		if self.val == 0:
			txt = Settings.menu_font.render(self.inf, 1, (255,255,255))
		else:
			txt = Settings.menu_font.render("%d" %(self.val), 1, (255,255,255))
		rect = txt.get_rect()
		rect.midtop = (w / 2, 2.5 * Settings.MENU_LINEFEED)
		result.blit(txt, rect.topleft)

		pygame.draw.rect(result, (0,0,200), pygame.Rect(0, 0, w, h), 1)

		return result


class Confirm(Menu):

	def __init__(self, txt1, txt2 = "", txt3 = ""):
		Menu.__init__(self, "")
		self.txt1 = txt1
		self.txt2 = txt2
		self.txt3 = txt3

	def draw(self):
		offset = 0

		w = self.get_width()
		h = self.get_height()
		result = pygame.Surface((w, h))
		#result.fill((100,0,0))
		result.blit(Settings.menu_background, (0,0))

		txt = Settings.menu_font.render(self.txt1, 1, (255,255,255))
		rect = txt.get_rect()
		rect.midtop = (w / 2, Settings.MENU_LINEFEED)
		result.blit(txt, rect.topleft)

		if self.txt2 != "":
			offset += Settings.MENU_LINEFEED
			txt = Settings.menu_font.render(self.txt2, 1, (255,255,255))
			rect = txt.get_rect()
			rect.midtop = (w / 2, Settings.MENU_LINEFEED + offset)
			result.blit(txt, rect.topleft)

		if self.txt3 != "":
			offset += Settings.MENU_LINEFEED
			txt = Settings.menu_font.render(self.txt3, 1, (255,255,255))
			rect = txt.get_rect()
			rect.midtop = (w / 2, Settings.MENU_LINEFEED + offset)
			result.blit(txt, rect.topleft)

		for i in xrange(0, 2):
			if i == self.selected:
				color = (self.count,self.count,255)
			else:
				color = (0,0,255)
			txt = Settings.menu_font.render(self.items[i][0], 1, color)
			rect = txt.get_rect()
			if i == 0:
				rect.topright = (w / 2 - Settings.MENU_LINEFEED, 3 * Settings.MENU_LINEFEED + offset)
			else:
				rect.topleft = (w / 2 + Settings.MENU_LINEFEED, 3 * Settings.MENU_LINEFEED + offset)
			result.blit(txt, rect.topleft)

		pygame.draw.rect(result, (0,0,200), pygame.Rect(0, 0, w, h), 1)

		self.count += self.inc
		if self.count > 255 or self.count < 0:
			self.inc *= -1
			self.count += 2* self.inc


		return result
