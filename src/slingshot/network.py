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

import socket
import sys
try:
	import cPickle as pickle
except:
	import pickle


class Network:

	def __init__(self, port, buf_size = 4096, debug = False):
		self.debug = debug
		self.port = port
		self.buf_size = buf_size

	def wait_for_cnct(self):
		try:
			for res in socket.getaddrinfo(None, self.port, socket.AF_UNSPEC,
						      socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
				af, socktype, proto, canonname, sa = res
				try:
					connect_s = socket.socket(af, socktype, proto)
				except socket.error, msg:
					connect_s = None
					continue
				try:
					connect_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
					connect_s.bind(sa)
					connect_s.listen(1)
					connect_s.settimeout(2)
				except socket.error, msg:
					connect_s.close()
					connect_s = None
					continue
				break
		except socket.error, msg:
			connect_s = None

		if connect_s is None:
			print(msg)
			return False

		try:
			(self.s, self.addr) = connect_s.accept()
			self.w_stream = self.s.makefile('wb')
			self.r_stream = self.s.makefile('rb')
			connect_s.close()
		except:
			connect_s.close()
			return -1

	def cnct(self, hostname):
		try:
			for res in socket.getaddrinfo(hostname, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM):
				af, socktype, proto, canonname, sa = res
				try:
					self.s = socket.socket(af, socktype, proto)
				except socket.error, msg:
					self.s = None
					continue
				try:
					self.s.settimeout(3)
					self.s.connect(sa)
				except socket.error, msg:
					self.s.close()
					self.s = None
					continue
				break
		except socket.error, msg:
			self.s = None

		if self.s is None:
			print(msg)
			return False
		else:
			self.s.settimeout(None)
			self.w_stream = self.s.makefile('wb')
			self.r_stream = self.s.makefile('rb')

	def send(self, data):
		if self.debug: print(data)
		try:
			pickle.dump(data ,self.w_stream, 1)
			self.w_stream.flush()
		except BaseException as be:
			print(be)
			return False

	def recv(self):
		try:
			data = pickle.load(self.r_stream)
			if self.debug: print(data)
			return data
		except BaseException as be:
			print(be)
			return False

	def close(self):
		try:
			self.r_stream.close()
		except:
			pass
		try:
			self.w_stream.close()
		except:
			pass
		try:
			self.s.close()
		except:
			pass

	def __del__(self):
		self.close()
