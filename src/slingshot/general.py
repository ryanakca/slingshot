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
from pygame.locals import *
from math import sqrt
import os.path

from slingshot.settings import Settings

def load_image(name, colorkey=None):
	fullname = os.path.join(Settings.DATA_PATH, name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error as message:
		print('Cannot load image:', fullname)
		raise SystemExit(message)
	image = image.convert_alpha()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

#def sgn(x):
#	if x < 0:
#		return -1
#	else:
#		return 1

#def get_intersect(center, r, pos1, pos2):
#	dx = pos2[0] - pos1[0]
#	dy = pos2[1] - pos1[1]
#	dr = math.sqrt(dx**2 + dy**2)
#	D = pos1[0]*pos2[1] - pos2[0]*pos1[1]
#	delta = r**2 * dr**2 - D**2
#	if delta < 0:
#		return (0.0,0.0)
#	x = center[0] + (D * dy + sgn(dy) * dx * math.sqrt(delta)) / dr**2
#	y = center[1] + (-D * dx + abs(dy) * math.sqrt(delta)) / dr**2
#	return (x,y)

def get_intersect(center, r, pos1, pos2):
	dx = pos2[0] - pos1[0]
	dy = pos2[1] - pos1[1]
	px = pos1[0]
	py = pos1[1]
	cx = center[0]
	cy = center[1]
	a = dx**2 + dy**2
	b = 2 * (dx * px - dx * cx + dy * py - dy * cy)
	c = -2 * cx * px -2 * cy * py + px**2 + py**2 + cx**2 + cy**2 - r**2
	D = b**2 - 4 * a * c
#	print(center, r)
#	print(pos1, pos2)
#	print(dx, dy)
#	print(a, b, c, D)
	if D < 0:
		return (4000.0, 3000.0)
	alpha = (-b + sqrt(D)) / (2 * a)
	if alpha > 1:
		alpha = (-b - sqrt(D)) / (2 * a)
	alpha = alpha - 0.05
	pos = (px + alpha * dx, py + alpha * dy)
#	print(pos)
	return pos

def get_data_path(file):
	return os.path.join(Settings.DATA_PATH, file)

def prep_text(text, antialias, font, linespacing, color):
	'''
	Let's make it easy to draw text.

	Input:
	  text: a list of lines to print.
	  antialias: Bool that controls antialiasing
	  font: An initialized pygames.font.Font object
	  linespacing: the number of pixels between lines
	  color: (R, G, B)
	Output:
	  A list of tuples in the format:
	  (surface, (line width, distance between the top of the first line
	  and the top of this line))
	'''
	text_surfaces = []
	text_height = 0
	for line in text:
		rendered_text = font.render(line, antialias, color)
		text_surfaces.append((rendered_text,
				(rendered_text.get_width(), text_height)
					))
		# So that we place the next line directly under this one:
		text_height += rendered_text.get_height()
		text_height += linespacing
	return text_surfaces
