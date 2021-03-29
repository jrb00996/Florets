# Florets
Python folder management for floret processing


# Installation:

## mac OS or Linux
1) To get started open command prompt, type "cd" with a space after and drag the "dist" folder in it. Press Enter
2) Copy and paste the following command without the quotes:

    "pip3 install ."

3) You are ready to go, run the command "florets" each time your start measuring or scanning.
and it will handle all of your files for you


## Windows
1) To get started open command prompt, type "cd" with a space after and drag the "dist" folder in it. Press Enter
2) Copy and paste the following command without the quotes:

    "pip3 install ."

3) You are ready to go, run the command "python3 -m florets.cli" each time your start measuring or scanning,
and it will handle all of your files for you



–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
## Functionality:
1) If it is your first time running it run the starting command above but with the "-- setup" flag at the end (just type a space and --setup), it will take you to a setup menu.
    a) First it will ask your for the file paths for three folders: Originals, Unmeasured, and Measured
    b) To copy the paths, click and drag the coresponding folder into the command line window and press enter.
2) Once running, the script will check every 3 seconds to see if there are any pictueres in originals that aren't in unmeasured or measured and copy them to unmeasured
3) Next it checks if there are files in measured that are also in unmeasured and removes them from unmeasured
4) Lastly it checks if there is a csv file that was stored in measured and moves it to archived_results and appends its contents to Master_record.csv

* if you have any questions, give me a call or try running the starting command with the "--help" flag
* if you do not have python installed on your computer, this script will not run. Go to www.python.org/downloads and follow the download instructions. This shouldn't take more than 5 to 10 minutes
