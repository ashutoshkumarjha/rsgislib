#!/usr/bin/env python
############################################################################
#  solarangles.py
#
#  Copyright 2016 RSGISLib.
#
#  RSGISLib: 'The remote sensing and GIS Software Library'
#
#  RSGISLib is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  RSGISLib is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with RSGISLib.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Purpose: Provide a set of utilities which provide further functionality
#          specifically for caclulating solar angles.
#
# Author: Pete Bunting
# Email: petebunting@mac.com
# Date: 23/11/2016
# Version: 1.0
#
# History:
# Version 1.0 - Created.
#
############################################################################

from osgeo import osr
import numpy


def get_solar_irr_convention_solar_azimuth_from_usgs(solarAz):
    """
    IN: USGS Convertion::

                  N (0)
                  |
         W (-90)-----E (90)
                  |
           (-180) S (180)

    OUT: Solar Irradiance Convertion::

                  N (0)
                  |
         W (270)-----E (90)
                  |
                  S (180)
    """
    solarAzOut = solarAz
    if solarAz < 0:
        solarAzOut = 360 + solarAz
    return solarAzOut


def get_solar_irr_convention_solar_azimuth_from_trad(solarAz):
    """
    IN: Traditional Convertion::

           (-180) N (180)
                  |
         W (-90)-----E (90)
                  |
                  S (0)

    OUT: Solar Irradiance Convertion::

                  N (0)
                  |
         W (270)-----E (90)
                  |
                  S (180)
    """
    solarAzOut = 0.0
    if solarAz > 0:
        solarAzOut = 180 - solarAz
    elif solarAz < 0:
        solarAzOut = 180 + ((-1) * solarAz)
    return solarAzOut


def calc_solar_azimuth_zenith(inputImg, inImgDateTime, outputImg, gdalformat):
    """
    Function which calculate a solar azimuth (band 1) and zenith (band 2) image.

    :param inputImg: input image file (can be any image with a spatial header)
    :param inImgDateTime: a datatime object for the data/time of the acquasition
    :param outputImg: output image file and path
    :param gdalformat: output file format (e.g., KEA)
    """
    import Pysolar
    from rios import applier
    from rios import cuiprogress
    import rsgislib

    try:
        import tqdm

        progress_bar = rsgislib.TQDMProgressBar()
    except:
        progress_bar = cuiprogress.GDALProgressBar()

    infiles = applier.FilenameAssociations()
    infiles.image1 = inputImg
    outfiles = applier.FilenameAssociations()
    outfiles.outimage = outputImg
    otherargs = applier.OtherInputs()
    otherargs.dateTime = inImgDateTime
    aControls = applier.ApplierControls()
    aControls.progress = progress_bar
    aControls.drivername = gdalformat

    wgs84latlonProj = osr.SpatialReference()
    wgs84latlonProj.ImportFromEPSG(4326)
    otherargs.wgs84latlonProj = wgs84latlonProj

    def _calcSolarAzimuthZenith(info, inputs, outputs, otherargs):
        """
        Internal functions used within calc_solar_azimuth_zenith() - don't call independently.

        """
        xBlock, yBlock = info.getBlockCoordArrays()

        inProj = osr.SpatialReference()
        inProj.ImportFromWkt(info.getProjection())

        transform = osr.CoordinateTransformation(inProj, otherargs.wgs84latlonProj)
        xBlockF = xBlock.flatten()
        yBlockF = yBlock.flatten()

        pts = numpy.zeros((xBlockF.shape[0], 2), dtype=numpy.float32)
        pts[..., 0] = xBlockF
        pts[..., 1] = yBlockF
        outPts = numpy.array(transform.TransformPoints(pts))

        outAz = numpy.zeros_like(xBlockF, dtype=numpy.float32)
        outZen = numpy.zeros_like(xBlockF, dtype=numpy.float32)

        for i in range(outPts.shape[0]):
            outAz[i] = 90 - Pysolar.solar.GetAltitude(
                outPts[i, 1], outPts[i, 0], otherargs.dateTime
            )
            outZen[i] = (
                (-1)
                * Pysolar.solar.GetAzimuth(
                    outPts[i, 1], outPts[i, 0], otherargs.dateTime
                )
            ) - 180

        outAz = numpy.reshape(outAz, xBlock.shape)
        outZen = numpy.reshape(outZen, xBlock.shape)

        # print("Block End")
        outputs.outimage = numpy.stack((outAz, outZen))

    # Apply the multiply function.
    applier.apply(
        _calcSolarAzimuthZenith, infiles, outfiles, otherargs, controls=aControls
    )
