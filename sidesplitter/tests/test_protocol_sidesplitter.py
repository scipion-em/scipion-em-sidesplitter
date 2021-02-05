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

from pyworkflow.utils import magentaStr, makePath, copyFile
from pyworkflow.tests import BaseTest, DataSet, setupTestProject
from pyworkflow.plugin import Domain
from pwem.objects import Volume
from pwem.protocols import ProtImportParticles, ProtImportVolumes

from ..protocols import ProtSideSplitter


try:
    ProtRelionCreateMask3D = Domain.importFromPlugin("relion.protocols",
                                                     "ProtRelionCreateMask3D",
                                                     doRaise=True)
    ProtRelionRefine3D = Domain.importFromPlugin("relion.protocols",
                                                 "ProtRelionRefine3D",
                                                 doRaise=True)
except ImportError as e:
    print("Relion plugin not found! You need to install it to be able to run this test.")


class TestSideSplitter(BaseTest):
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        cls.ds = DataSet.getDataSet('relion_tutorial')
        pathFns = 'import/refine3d/extra'
        cls.volFn = cls.ds.getFile(os.path.join(pathFns, 'relion_class001.mrc'))
        cls.half1Fn = cls.ds.getFile(os.path.join(pathFns, 'relion_it025_half1_class001.mrc'))
        cls.half2Fn = cls.ds.getFile(os.path.join(pathFns, 'relion_it025_half2_class001.mrc'))

    def importVolume(self):
        print(magentaStr("\n==> Importing data - volume:"))
        protVol = self.newProtocol(ProtImportVolumes,
                                   objLabel='import volume',
                                   filesPath=self.volFn,
                                   samplingRate=3)
        self.launchProtocol(protVol)
        return protVol

    def importPartsFromScipion(self):
        print(magentaStr("\n==> Importing data - particles:"))
        partFn = self.ds.getFile('import/particles.sqlite')
        protPart = self.newProtocol(ProtImportParticles,
                                    objLabel='Import Particles',
                                    importFrom=ProtImportParticles.IMPORT_FROM_SCIPION,
                                    sqliteFile=partFn,
                                    magnification=10000,
                                    samplingRate=3,
                                    haveDataBeenPhaseFlipped=True
                                    )
        self.launchProtocol(protPart)
        return protPart

    def _createRef3DProtBox(self, label, protocol):
        from pyworkflow.protocol.constants import STATUS_FINISHED

        prot = self.newProtocol(protocol)
        self.saveProtocol(prot)

        prot.setObjLabel(label)
        makePath(prot._getPath())
        makePath(prot._getExtraPath())
        makePath(prot._getTmpPath())

        prot.inputParticles.set(self.importPartsFromScipion().outputParticles)

        outputVol = self.importVolume().outputVolume
        prot.referenceVolume.set(outputVol)

        volume = Volume()
        volume.setFileName(prot._getExtraPath('test.mrc'))
        pxSize = prot.inputParticles.get().getSamplingRate()
        volume.setSamplingRate(pxSize)

        prot._defineOutputs(outputVolume=volume)
        prot.setStatus(STATUS_FINISHED)

        # Create a mask protocol
        print(magentaStr("\n==> Running relion - create mask 3d:"))
        protMask = self.newProtocol(ProtRelionCreateMask3D)
        protMask.inputVolume.set(outputVol)
        self.launchProtocol(protMask)

        return prot, protMask

    def _validations(self, vol, dims, pxSize):
        self.assertIsNotNone(vol, "There was a problem with sidesplitter "
                                  "protocol, using Relion auto-refine as input")
        xDim = vol.getXDim()
        sr = vol.getSamplingRate()
        self.assertEqual(xDim, dims, "The dimension of your volume is (%d)^3 "
                                     "and must be (%d)^3" % (xDim, dims))

        self.assertAlmostEqual(sr, pxSize, delta=0.0001,
                               msg="Pixel size of your volume is %0.2f and"
                                   " must be %0.2f" % (sr, pxSize))

    def test_sidesplitter(self):
        protRef, protMask = self._createRef3DProtBox("auto-refine",
                                                     ProtRelionRefine3D)
        protRef._createFilenameTemplates()
        volPath = protRef._getFileName('finalvolume', ref3d=1).split(':')[0]
        volHalf1 = protRef._getFileName('final_half1_volume', ref3d=1).split(':')[0]
        volHalf2 = protRef._getFileName('final_half2_volume', ref3d=1).split(':')[0]

        copyFile(self.volFn, volPath)
        copyFile(self.half1Fn, volHalf1)
        copyFile(self.half2Fn, volHalf2)

        protRef.outputVolume.setFileName(volPath)
        protRef.outputVolume.setHalfMaps([volHalf1, volHalf2])
        project = protRef.getProject()
        project._storeProtocol(protRef)

        print(magentaStr("\n==> Testing sidesplitter - after refine 3d:"))
        sidesplitterProt = self.newProtocol(ProtSideSplitter,
                                            protRefine=protRef,
                                            mask=protMask.outputMask)
        sidesplitterProt.setObjLabel('sidesplitter after Auto-refine')

        self.launchProtocol(sidesplitterProt)
        self._validations(sidesplitterProt.outputVolume1, 60, 3)
