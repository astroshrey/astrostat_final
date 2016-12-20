A longer description of this project is included in my final write-up.
Here, you can find the running sequence to emulate how I did this project.

NOTE: you will probably need to change the line at the top of each python script
if you use ./[scriptname] like I do.

NOTE2: All of the plots created by the scripts in this repo are sort of standard
matplotlib plots. I went back and refactored things in seaborn as I always do for
presentation and write-up purposes.

1. Run cross_reference.py to cross-ref the McQuillan dataset with the Mathur dataset and
institute the mass cutoff. This script populates crossref.txt with an new table. This
file is well commented.

2. Run diagnostic.py to make the diagnostic plot included in the final write-up. The axes
are a bit messy which is inevitable for a dataset of this many parameters. This file is
well commented.

3. Run envelope.py to perform the first k-folds polynomial cross-validation for the
envelope of Port vs. Teff. This file is well commented. 

NOTE: beyond this point, all of the files are very poorly commented, since they are
mostly clones of poorly commented versions of envelope.py. 

4. Run densenv.py, lumenvelope.py, massenv.py, metalenvelope.py and rperenvelope.py to get
the data and results seen in Section 4 of my final write-up. 

Please feel free to email sv2421@columbia.edu with any questions.
