#Add Lyrics
##Version 2.0
***************************************

(C) Brendan J. Herger
Analytics Master's Candidate at University of San Francisco
13herger@gmail.com

Available under MIT License
http://opensource.org/licenses/MIT


##OVERALL
**********************************

Basically, this is just a program to add lyrics to most of the files in your iTunes Library.

This program is mosly limited by the speed at which it can scrape from the lyrics website.

CURRENT IMPLEMENTATION-File I/O
**********************************
In its current state, this python file is set up to run with the command:

    python LyricGrabber.py -d directory


##CURRENT IMPLEMENTATION-Optimization
**********************************
The speed of this script is primarily limited by the speed at which lyric data can be scraped. This script is purposely 
slowed such that it does not spam the lyric website I've chosen (and does not have its requests denied). 
