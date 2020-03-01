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

import pyworkflow.protocol.params as params
import pyworkflow.utils as pwutils
from pwem.protocols import ProtAnalysis3D
from pwem.objects import Volume
from pwem.emlib.image import ImageHandler

import sidesplitter
from ..convert import convertMask


class ProtSideSplitter(ProtAnalysis3D):
    """
    Protocol for mitigating local over-fitting by filtering.
     
    Find more information at https://github.com/StructuralBiology-ICLMedicine/SIDESPLITTER
    """
    _label = 'local filter'

    def _getInputPath(self, *paths):
        return self._getPath('input', *paths)

    def _initialize(self):
        """ This function is meant to be called after the
        working dir for the protocol have been set.
        (maybe after recovery from mapper)
        """
        self._createFilenameTemplates()

    def _createFilenameTemplates(self):
        """ Centralize how files are called for iterations and references. """
        myDict = {'half1': self._getInputPath("half1_unfil.mrc"),
                  'half2': self._getInputPath("half2_unfil.mrc"),
                  'mask': self._getInputPath("mask.mrc"),
                  'outHalf1Fn': self._getExtraPath('halfmap1.mrc'),
                  'outHalf2Fn': self._getExtraPath('halfmap2.mrc'),
                  }

        self._updateFilenamesDict(myDict)

    # --------------------------- DEFINE param functions ----------------------

    def _defineParams(self, form):
        form.addSection(label='Input')
        form.addParam('protRefine', params.PointerParam,
                      important=True,
                      pointerClass="ProtRefine3D",
                      label='Select a previous refinement protocol',
                      help='Select any previous refinement protocol to get the '
                           '3D half maps. Note that the refinement protocol '
                           'must use gold-standard method.')
        form.addParam('mask', params.PointerParam,
                      allowsNull=True,
                      pointerClass="VolumeMask",
                      label='Volume mask',
                      help="Provide the mask used in 3D refinement.")
        form.addParam('doSNRWeighting', params.BooleanParam,
                      expertLevel=params.LEVEL_ADVANCED,
                      default=False,
                      label='Use SNR-weighted spectrum',
                      help='Outputs the SNR weighted spectrum rather '
                           'than matching input spectrum / grey-scale.')

        form.addParallelSection(threads=1, mpi=0)

    # --------------------------- INSERT steps functions ----------------------
    
    def _insertAllSteps(self):
        objId = self.protRefine.get().getObjId()
        self._initialize()
        self._insertFunctionStep('convertInputStep', objId)
        self._insertFunctionStep('runSideSplitterStep')
        self._insertFunctionStep('createOutputStep')

    # --------------------------- STEPS functions -----------------------------
    
    def convertInputStep(self, protId):
        """ Convert input half-maps to mrc as expected by SIDESPLITTER."""
        pwutils.makePath(self._getInputPath())

        protRef = self.protRefine.get()
        outVol = protRef.outputVolume
        dim = outVol.getXDim()
        vols = outVol.getHalfMaps().split(',')
        ih = ImageHandler()

        if self.mask.hasValue():
            convertMask(self.mask.get(), self._getFileName('mask'), newDim=dim)

        for vol, key in zip(vols, ['half1', 'half2']):
            ih.convert(vol, self._getFileName(key))

    def runSideSplitterStep(self):
        """ Call SIDESPLITTER with the appropriate parameters. """
        args = self._getArgs()
        param = ' '.join(['%s %s' % (k, str(v)) for k, v in args.items()])
        program = sidesplitter.Plugin.getProgram()
        cmd = 'export OMP_NUM_THREADS=%d; ' % self.numberOfThreads.get()
        cmd += program

        self.runJob(cmd, param, env=sidesplitter.Plugin.getEnviron(),
                    cwd=self._getExtraPath(),
                    numberOfThreads=1)

    def createOutputStep(self):
        inputVol = self.protRefine.get().outputVolume
        ps = inputVol.getSamplingRate()

        vol = Volume()
        vol.setSamplingRate(ps)
        vol.setObjLabel('Filtered half-map 1')
        vol.setFileName(self._getFileName('outHalf1Fn'))

        vol2 = Volume()
        vol2.setSamplingRate(ps)
        vol2.setObjLabel('Filtered half-map 2')
        vol2.setFileName(self._getFileName('outHalf2Fn'))

        outputs = {'outputVolume1': vol,
                   'outputVolume2': vol2}
        self._defineOutputs(**outputs)
        self._defineSourceRelation(inputVol, vol)
        self._defineSourceRelation(inputVol, vol2)

    # --------------------------- INFO functions ------------------------------
    
    def _summary(self):
        summary = []

        return summary
    
    def _validate(self):
        errors = []

        return errors
    
    # --------------------------- UTILS functions -----------------------------
 
    def _getArgs(self):
        import os
        """ Prepare the args dictionary."""
        args = {'--v1': self._getPaths(self._getFileName('half1')),
                '--v2': self._getPaths(self._getFileName('half2'))}

        if self.mask.hasValue():
            args.update({'--mask': self._getPaths(self._getFileName('mask'))})

        if self.doSNRWeighting:
            args.update({'--spectrum': ' '})

        return args

    def _getPaths(self, fn):
        """ Return relative path to the input dir from cwd=extra. """
        return pwutils.join("../input", os.path.basename(fn))
