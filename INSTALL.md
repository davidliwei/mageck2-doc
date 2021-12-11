# Installation

## Prerequisites

mageck2 needs the following packages for proper running:

* numpy
* scipy
* R/Rstudio (optional; only if you need to generate html files from R Markdown files)

## Installation from github

### Step 1: download the source code

Either download the zip file directly from [mageck2](https://github.com/davidliwei/mageck), 
or use the git clones command in your termincal:

    git clone https://github.com/davidliwei/mageck2.git
    

### Step 2: installation 

After that, invoke python setup.py:


    python setup.py install


For linux users without root privileges:


    python setup.py install --user
 
### Step 3: test whether the installation is successful

In your command line, type 

    mageck2
    
to see if it works. If an "Command not found" error shows up, go to Step 4 for path set up

### Setp 4: set up the environment variables

**In most systems you don't need to set up the environment variables. Just type "mageck2" in the command line to see if it is needed.**

If you get a "command not found" error, that indicates the environment variables are not properly set up. There are several additional steps to finish the installation. 
First you need to add the path of the mageck2 program to your **PATH** variable. 


If you use the --user option during installation (or other situations), 
first determine where mageck2 is installed. 
See this [Q and A](https://sourceforge.net/p/mageck/wiki/QA/#where-is-mageck-binary-installed) for additional steps to determine the correct bin directory.

If your bin directory is located in */Users/john/.local/bin*, then type the following:


    export PATH=$PATH:/Users/john/.local/bin


