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

from .constants import SIDESPLITTER_HOME, V1_2

__version__ = '3.0.10'
_logo = "sidesplitter_logo.png"
_references = ['Ramlaul2020']


class Plugin(pwem.Plugin):
    _homeVar = SIDESPLITTER_HOME
    _pathVars = [SIDESPLITTER_HOME]
    _supportedVersions = V1_2
    _url = "https://github.com/scipion-em/scipion-em-sidesplitter"

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(SIDESPLITTER_HOME, 'sidesplitter-1.2')

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
        SW_EM = env.getEmFolder()
        url = 'https://github.com/StructuralBiology-ICLMedicine/SIDESPLITTER/archive/master.zip'
        installCmd = [
            'wget %s && unzip master.zip &&' % url,
            'cd SIDESPLITTER-master &&',
            'gcc -O3 *.c -lm -pthread -lfftw3 -lfftw3_threads -std=c99 -o sidesplitter && mv sidesplitter ../'
        ]

        commands = [(" ".join(installCmd),
                     '%s/sidesplitter-1.2/sidesplitter' % SW_EM)]

        env.addPackage('sidesplitter', version='1.2',
                       tar='void.tgz',
                       neededProgs=['unzip', 'gcc'],
                       commands=commands,
                       default=True)
