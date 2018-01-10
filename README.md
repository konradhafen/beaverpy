#BDWS (Beaver Dam Water Storage)

####[>>> Full documentation <<<](https://konradhafen.github.io/beaver-dam-water-storage/)

See the [full documentation](https://konradhafen.github.io/beaver-dam-water-storage/) 
for detailed [installation instructions](https://konradhafen.github.io/beaver-dam-water-storage/install.html),
[usage information](https://konradhafen.github.io/beaver-dam-water-storage/useage.html),
[tutorials](https://konradhafen.github.io/beaver-dam-water-storage/example.html),
and [code description](https://konradhafen.github.io/beaver-dam-water-storage/code.html).

####[>>> Full documentation <<<](https://konradhafen.github.io/beaver-dam-water-storage/)

BDWS is composed of three python classes which allow for spatial estimation of water 
storage created from the construction of beaver dams. The `BDLoG` class uses results
from the [BRAT model](http://brat.joewheaton.org) to generate dam locations along a stream
network. `BDLoG` also generates dam heights for each dam location from empirical 
distributions of measured beaver dam heights. The `BDSWEA` class uses dam locations and 
dam heights to estimate the area inundated by these beaver dams, and the volume of water 
each resulting pond might store. The `BDflopy` class uses the existing 
[FloPy](https://modflowpy.github.io/flopydoc/) moduleto parameterize 
[MODFLOW-2005](https://water.usgs.gov/ogw/modflow/mf2005.html) to estimate how these dams 
may also affect groundwater storage.

##How to use BDWS

###Dependencies

**Python version:** 2.7.x <br>
**Python modules:** gdal, numpy, flopy <br>
**Programs:** MODFLOW-2005 

###Installation

The entire repository can be cloned to your machine directly from github, downloaded as 
a compressed folder, or individual files can be downloaded. 
Repository directories and files are described below.

- docs/
  - contains the pages for this documentation website
- sphinx/
  - contains the source code for building documentation website pages with the `sphinx` module
- tutorials/
  - contains data for use in the BDWS tutorials
- bdws.py
  - source code for the `BDLoG` and `BDSWEA` classes
- bdflopy.py
  - source code for the `BDflopy` class
- run.py
  - example script for usage of BDWS

`BDflopy` code is in a separate file because it requires use of MODFLOW-2005 and the `flopy` module.
Some users may wish to use `BDLoG` and/or `BDSWEA` without `BDflopy`.

To clone the github repository, enter the following from a terminal.

    $ cd /path/to/project
    $ git clone https://github.com/konradhafen/beaver-dam-water-storage

This will create a new directory containing everything in the repository at the location:

    /path/to/project/beaver-dam-water-storage
    
###General usage

Currently, it is recommended to use BDWS to create python scripts to model beaver dam 
water storage.BDWS has been developed and tested using the 
`PyCharm IDE <https://www.jetbrains.com/pycharm/>`_.
Below are brief examples describing how to use BDWS classes. For more detailed examples 
of BDWS implementation visit the `tutorials <example.html>`_ page of the documentation.

BDWS code is hosted at https://github.com/konradhafen/beaver-dam-water-storage in the 
`bdws.py` and `bdflopy.py` files. Classes can be imported as follows.

    from bdws import*
    from bdflopy import *

`BDLoG` takes a vector stream network created by 
`BRAT <http://brat.joewheaton.org>`_ and generates locations of individual dams on a 
rasterized stream network.

Initialization of `BDLoG` requires a shapefile created by 
`BRAT <http://brat.joewheaton.org>`_, a DEM, a rasterized stream network, path to output 
directory, and a proportion of maximum dam capacity to model. The following code will 
initialize `BDLoG`, generate dam locations
and dam heights, and save output files for a maximum capacity (1.0) scenario.

    model = BDLoG('path/to/brat.shp', 'path/to/dem.tif', 'path/to/fac.tif', 'out/dir', 1.0)
    model.run()
    modle.close()

`BDSWEA` uses dam locations and dam heights generated by `BDLoG` to estimate 
the area and surface volume created by beaver dam construction.

`BDSWEA` requires output files (see below) from `BDLoG` for initialization. 
`BDSWEA` initialization requires a DEM, a flow direction raster derived from the 
DEM, a rasterized stream network, the dam ID raster created by
`BDLoG`, an output directory, the dam location and attribute shapefile created by 
`BDLoG`. The following code will estimate beaver pond inundation and write files 
necessary for parameterization of MODFLOW.

    model = BDSWEA('path/to/dem.tif', 'path/to/fdir.tif', 'path/to/fac.tif', 'path/to/id.tif',
                    'out/dir', 'path/to/pts.shp')
    model.run()
    model.writeModflowFiles()
    model.close()

`BDflopy` implements the existing `FloPy module <https://modflowpy.github.io/flopydoc/>`_ to automatically
parameterize MODFLOW-2005 to estimate changes to goundwater storage resulting from 
beaver dam construction.

`BDflopy` requires the path to a MODFLOW-2005 executable, path to directory of 
input rasters, path to directory
of `BDSWEA` outputs, path to directory to write outputs, and name of DEM file in 
inputs directory for initialization. The following code will initialize `BDflopy`.

    model = BDflopy('path/to/modflow.exe', 'input/dir', 'bdswea/out/dir', 'out/dir', 'dem.tif')

`BDflopy.run()` requires additional parameters. Horizontal and vertical hydraulic conductivity (as a raster,
numpy array, or single value), a factor to convert conductivity values to meters per second, the fraction of soil
available for water storage (e.g. field capacity or porosity), and a factor to convert the soil fraction to a proportion.
This will write MODFLOW's input files, run MODFLOW, and generate output raster files.
`BDflopy.run()` can be implemented as follows.

    model.run('path/to/hk.tif', 'path/to/vk.tif', 1.0, 'path/to/frac.tif', 1.0)
    #or
    model.run(1.0, 1.0, 0.000001, 20.0, 0.01)

Then close the class object.

    model.close()
