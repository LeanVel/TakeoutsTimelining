# TakeoutsTimelining
The idea of this project is to permom a forensics analysis on the available data on Google Takeout by doing timelining. This tool was written in python and at the moment it has some \*nix dependencies on the hashing and the decompressing functions.

## Installation Requirments
sudo apt install python3-pip

pip3 install icalendar
Edit

## Usage
'''
  ./MainProgram.py -h
    
    Usage: MainProgram.py [options] <TakeOut File(s)>

    Options:
      -h, --help            show this help message and exit
      -d DESTDIR, --dest-dir=DESTDIR
                            specify destination directory to decompress 
                            the takeout file
                            
      -o OUTDIR, --output-dest-dir=OUTDIR
                            specify destination directory to save 
                            the output files
                            
      -p OUTPREFIX, --output-prefix=OUTPREFIX
                            specify the output files prefix
                            
      -b BEGINTIMEFRAME, --beging-time-frame=BEGINTIMEFRAME
                            specify the beginning of the desired                             
                            time frame in the format YYYY-MM-DD hh:mm
                            
      -e ENDTIMEFRAME, --end-time-frame=ENDTIMEFRAME
                            specify the end of the desired time frame in 
                            the format YYYY-MM-DD hh:mm
'''                            
                            
## Examples 
In this repository you can find a Google Takeout exaple so you can test this tool.

'''./MainProgram.py takeout-20170310T190539Z-001.zip'''

This tool also suppors Unix wildcards and user environmental variables such as "~"

'''./MainProgram.py ~/takeout-20170310T190539Z-00*'''
