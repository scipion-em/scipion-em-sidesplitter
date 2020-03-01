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

import pyworkflow.utils as pwutils
from pwem.emlib.image import ImageHandler


def getImageLocation(location):
    return ImageHandler.locationToXmipp(location)


def convertMask(img, outputPath, newDim=None):
    """ Convert binary mask to a format read by Relion and truncate the
    values between 0-1 values, due to Relion only support masks with this
    values (0-1).
    Params:
        img: input image to be converted.
        outputPath: it can be either a directory or a file path.
            If it is a directory, the output name will be inferred from input
            and put into that directory. If it is not a directory,
            it is assumed is the output filename.
    Return:
        new file name of the mask.
    """

    ih = ImageHandler()
    imgFn = getImageLocation(img.getLocation())

    if os.path.isdir(outputPath):
        outFn = os.path.join(outputPath, pwutils.replaceBaseExt(imgFn, 'mrc'))
    else:
        outFn = outputPath

    ih.truncateMask(imgFn, outFn, newDim=newDim)

    return outFn
