# TakeoutsTimelining
The idea of this project is to perform a forensics analysis on the available data on Google Takeout by doing timelining. This tool can process the .zip files from the Google Takeout service and create a basic timeline. Please keep in mind that all timestamps in the timeline are shown as UTC time. This tool was written in python and at the moment it has some \*nix dependencies on the hashing and the decompressing functions.

## Warning
Please keep in mind that this tool was created in a few afternoons as a students project. It is made as a proof of concept. If you ever use this tool for any investigation you have the obligation to check all the results. 

## Dependencies Installation
```
sudo apt install python3-pip

pip3 install icalendar

```

## Usage
```
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
```                         
                            
## Examples 
In this repository you can find a Google Takeout exaple so you can test this tool.

```
./MainProgram.py takeout-20170310T190539Z-001.zip 
```

This tool also suppors Unix wildcards and user environmental variables such as "~"

```
./MainProgram.py ~/takeout-20170310T190539Z-00*
```
![Timeline](https://cloud.githubusercontent.com/assets/17178504/24331666/6f04315e-1239-11e7-92ef-6f61c1b61ee5.png)

![Map](https://cloud.githubusercontent.com/assets/17178504/24331665/6f01e6b0-1239-11e7-8a3c-950e69baecfc.png)


