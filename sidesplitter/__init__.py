# **************************************************************************
# *
# * Authors:     Grigory Sharov (gsharov@mrc-lmb.cam.ac.uk)
# *
# * MRC Laboratory of Molecular Biology (MRC-LMB)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os

import pwem
from pyworkflow.utils import Environ

from .constants import SIDESPLITTER_HOME, V1_0


_logo = "sidesplitter_logo.png"
_references = ['Ramlaul2020']


class Plugin(pwem.Plugin):
    _homeVar = SIDESPLITTER_HOME
    _pathVars = [SIDESPLITTER_HOME]
    _supportedVersions = [V1_0]

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(SIDESPLITTER_HOME, 'sidesplitter-1.0')

    @classmethod
    def getEnviron(cls):
        """ Setup the environment variables needed to launch sidesplitter. """
        environ = Environ(os.environ)
        environ.update({'PATH': cls.getHome()}, position=Environ.BEGIN)
        return environ

    @classmethod
    def getProgram(cls):
        """ Return the program binary that will be used. """
        cmd = cls.getHome('sidesplitter')
        return str(cmd)

    @classmethod
    def defineBinaries(cls, env):
        shell = os.environ.get("SHELL", "bash")
        installcmd = [('%s compile.sh' % shell,
                       ['sidesplitter'])]

        env.addPackage('sidesplitter', version='1.0',
                       tar='sidesplitter_v1.0.tgz',
                       commands=installcmd,
                       default=True)
