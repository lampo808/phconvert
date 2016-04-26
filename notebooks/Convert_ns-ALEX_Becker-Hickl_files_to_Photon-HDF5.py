
# coding: utf-8

# # Convert ns-ALEX Becker-Hickl SPC/SET files to Photon-HDF5
# <p class="lead">This <a href="https://jupyter.org/">Jupyter notebook</a>
# will guide you through the conversion of a ns-ALEX data file from <b>SPC/SET</b>
# to <a href="http://photon-hdf5.org">Photon-HDF5</a> format. For more info on how to edit
# a jupyter notebook refer to <a href="http://nbviewer.jupyter.org/github/jupyter/notebook/blob/master/docs/source/examples/Notebook/Notebook%20Basics.ipynb#Overview-of-the-Notebook-UI">this example</a>.</p>
#
# <i>Please send feedback and report any problem to the
# [Photon-HDF5 google group](https://groups.google.com/forum/#!forum/photon-hdf5).</i>
#
# # 1. How to run it?
#
# The notebook is composed by "text cells", such as this paragraph, and "code cells"
# containing the code to be executed (and identified by an `In [ ]` prompt).
# To execute a code cell, select it and press **SHIFT+ENTER**.
# To modify an cell, click on it to enter "edit mode" (indicated by a green frame),
# then type.
#
# You can run this notebook directly online (for demo purposes), or you can
# run it on your on desktop. For a local installation please refer to:
#
# - [Jupyter Notebook Quick-Start Guide](http://jupyter-notebook-beginner-guide.readthedocs.org)
#
# <br>
# <div class="alert alert-info">
# Please run each each code cell using <b>SHIFT+ENTER</b>.
# </div>
#
# # 2. Prepare the data file
#
# ## 2.1 Upload the data file
#
# <br>
# <div class="alert alert-info">
# <b>Note:</b> if you are running the notebook locally skip to section <b>2.2</b>.
# </div>
#
# Before starting, you have to upload a data file to be converted to Photon-HDF5.
# You can use one of our example data files available
# [on figshare](http://dx.doi.org/10.6084/m9.figshare.1455963).
#
# To upload a file (up to 35 MB) switch to the "Home" tab in your browser,
# click the upload button and select the data file.
# Wait until the upload completes.
# For larger files (like some of our example files) please use the
# [Upload notebook](Upload data files.ipynb) instead.
#
# Once the file is uploaded, come back here and follow the instructions below.
#
# ## 2.2 Select the file
#
# Specify the input data file in the following cell:

# In[ ]:

filename = 'dsdna_d7d17_50_50_1.spc'


# The next cell will check if the `filename` is correct:

# In[ ]:

import os
try:
    with open(filename): pass
    print('Data file found, you can proceed.')
except IOError:
    print('ATTENTION: Data file not found, please check the filename.\n'
          '           (current value "%s")' % filename)


# In case of file not found, please double check the file name
# and that the file has been uploaded.

# # 3. Load the data
#
# We start by loading the software:

# In[ ]:

import matplotlib
#matplotlib.use("Agg")


# In[ ]:

import numpy as np


# In[ ]:

import tables


# In[ ]:

import matplotlib.pyplot as plt


# In[ ]:

import phconvert as phc


# In[ ]:

print('phconvert version: ' + phc.__version__)


# In[ ]:


# Then we load the input file:

# In[ ]:

d, meta = phc.loader.nsalex_bh(filename,
                               donor = 4,
                               acceptor = 6,
                               alex_period_donor = (1800, 3300),
                               alex_period_acceptor = (270, 1500),
                               excitation_wavelengths = (532e-9, 635e-9),
                               detection_wavelengths = (580e-9, 680e-9),)


# And we plot the `nanotimes` histogram:

# In[ ]:

phc.plotter.alternation_hist(d)


# The previous plot is the `nanotimes` histogram for the donor and acceptor channel separately.
# The shaded areas marks the donor (*green*) and acceptor (*red*) excitation periods.
#
# If the histogram looks wrong in some aspects (no photons, wrong detectors
# assignment, wrong period selection) please go back to the previous cell
# which loads the file and change the parameters until the histogram looks correct.

# You may also find useful to see how many different detectors are present
# and their number of photons. This information is shown in the next cell:

# In[ ]:

detectors = d['photon_data']['detectors']

print("Detector    Counts")
print("--------   --------")
for det, count in zip(*np.unique(detectors, return_counts=True)):
    print("%8d   %8d" % (det, count))


# # 4. Metadata
#
# In the next few cells, we specify some metadata that will be stored
# in the Photon-HDF5 file. Please modify these fields to reflect
# the content of the data file:

# In[ ]:

author = 'John Doe'
author_affiliation = 'Research Institution'
description = 'A demonstrative smFRET-nsALEX measurement.'
sample_name = '50-50 mixture of two FRET samples'
dye_names = 'ATTO550, ATTO647N'
buffer_name = 'TE50'


# # 5. Conversion
# <br>
# <div class="alert alert-success">
# <p>Once you finished editing the the previous sections you can proceed with
# the actual conversion. To do that, click on the menu <i>Cells -> Run All Below</i>.
#
# <p>After the execution go to <b>Section 6</b> to download the Photon-HDF5 file.
# </div>
#
# The cells below contain the code to convert the input file to Photon-HDF5.

# ## 5.1 Add metadata

# In[ ]:

d['description'] = description

d['sample'] = dict(
    sample_name=sample_name,
    dye_names=dye_names,
    buffer_name=buffer_name,
    num_dyes = len(dye_names.split(',')))

d['identity'] = dict(
    author=author,
    author_affiliation=author_affiliation)


# For completeness, we also store all the raw metadata from SET file in a user group:

# In[ ]:

d['user'] = {'becker_hickl': meta}


# ## 5.2 Save to Photon-HDF5
#
# This command saves the new file to disk. If the input data does not follows the Photon-HDF5 specification it returns an error (`Invalid_PhotonHDF5`) printing what violates the specs.

# In[ ]:

phc.hdf5.save_photon_hdf5(d, overwrite=True)


# You can check it's content by using an HDF5 viewer such as [HDFView](https://www.hdfgroup.org/products/java/hdfview/).
#
# # 6. Load Photon-HDF5
#
# We can load the newly created Photon-HDF5 file to check its content:

# In[ ]:

from pprint import pprint


# In[ ]:

filename = d['_data_file'].filename


# In[ ]:

h5data = phc.hdf5.load_photon_hdf5(filename)


# In[ ]:

phc.hdf5.dict_from_group(h5data.identity)


# In[ ]:

phc.hdf5.dict_from_group(h5data.setup)


# In[ ]:

pprint(phc.hdf5.dict_from_group(h5data.photon_data))


# In[ ]:

h5data._v_file.close()
