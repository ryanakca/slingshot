Slingshot v0.8.1p

http://www.slingshot-game.org

This package contains the python source which can be executed with the python interpreter (also requires python-pygame).

Report any bugs, read the documentation, comment, submit ideas or get involved at www.slingshot-game.org

--- Changelog ---

Fixed a small bug which some people experienced where one ship would change position to the top left corner of the game screen during play.

--- Requirements ---

python 2.4 (or higher)			http://www.python.org/
python-pygame 1.7.1 (or higher)		http://www.pygame.org/


--- Installation / Running ---

Simply move the contents of the directory 'slingshot' to wherever you want, ch into it and execute with the command:
python slingshot.py

If you wish to install system wide, it is suggested that you copy the slingshot directory to /opt and then create a script named 'slingshot' and place it in /usr/bin.  The script should consist of something like:

	#!/bin/bash
	#
	cd /opt/slingshot
	python slingshot.py
	exit


--- Credit/Contact ---

Slingshot was created by Jonathan Musther and Bart Mak.
Visit www.slingshot-game.org
E-mail jon@slingshot-game.org


--- Copyright/Licensing ---

Slingshot is a two-dimensional strategy game where two players attempt to shoot one another through a section of space populated by planets.  The main feature of the game is that the shots, once fired, are affected by the gravity of the planets.

Slingshot is Copyright 2007 Jonathan Musther and Bart Mak. It is released under the terms of the GNU General Public License version 2, or later if applicable.

Slingshot is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or any later version.

Slingshot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Slingshot; if not, write to:
The Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA


