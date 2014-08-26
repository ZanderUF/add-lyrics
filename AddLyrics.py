# idGrabber.py
# (C) Brendan J. Herger
# Analytics Master's Candidate at University of San Francisco
# 13herger@gmail.com
#
# Available under MIT License
# http://opensource.org/licenses/MIT
#
# *********************************
import multiprocessing

__author__ = 'bjherger'

# imports
############################################

#mine
import bhUtilties
import LyricGrabber

#others
import argparse
import os
import numpy as np
import string


#specific
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, USLT
from mutagen.mp3 import MP3

#import setup
# variables
############################################

# functions
############################################


def parseArgument():
    """
    Parse command line arguments provided in the form -k value
    :return: A dicitonary, of the form { K : value}
    :rtype: dict
    """
    parser = argparse.ArgumentParser(description='Parsing a file.')
    parser.add_argument('-d', nargs=1, required=True)
    args = vars(parser.parse_args())
    return args


def get_tag(file):
    """
    Returns the id3 tag information for the given file, if possible
    :param file: File whose id3 information is desired
    :return: dictionary of the form: {id3 tag : id3 value}
    """
    return_dict = dict()
    if file.endswith(".mp3"):
        audio = MP3(file)
        return_dict["length"] = audio.info.length
        return_dict["bitrate"] = audio.info.bitrate
        audio = EasyID3(file)
        for (key, value) in audio.iteritems():
            if len(value) == 1:
                return_dict[key] = filter(lambda x: x in string.printable, value[0])
            else:
                return_dict[key] = [filter(lambda x: x in string.printable, localString) for localString in value]
    return return_dict

def set_lyrics(file):
    """
    Set the lyrics for the given file, if possible.
    :param file: file to add lyrics to
    :return: None
    """

    # get meta information to search for lyrics
    audio = ID3(file)
    artist = EasyID3(file)["artist"][0]
    title = EasyID3(file)["title"][0]

    # variables
    lyrics = ""
    completed = False

    #loop until failed or complete (ignoring website rejecting request)
    while not completed:
        try:

            #get lyrics
            lyrics = LyricGrabber.get_lyrics(artist, title)
            completed = True

            print "accepted, ",
            print file

        except Exception, e:

            lyrics = "None Found"
            #if lyrics not found due to server reject, keep trying
            if str(e) != "HTTP Error 503: Service Temporarily Unavailable":
                completed = True
            # else:
                # print "rejected, ",

    #add lyrics, save
    audio.add(USLT(encoding=3, text=lyrics))
    audio.save()


def walk_path(directory):
    """
    Recursively generates list of files within given directory
    :param directory: directory to walk
    :return: list of files, with each file in full path.
    """
    file_list = []
    for root, dir, files in os.walk(directory):
        files = [os.path.join(root, file) for file in files]
        file_list.extend(files)
    return file_list

def add_lyrics(file_list):
    """
    Add lyrics to files in file_list, if possible.
    :param file_list: list of files to add lyrics to
    :return:
    """

    print ".",
    for file in file_list:
        try:
            set_lyrics(file)
        except:
            pass



#main
############################################

if __name__ == "__main__":
    print "Begin Main"
    bhUtilties.timeItStart(printOff=False)

    #get file list
    args = parseArgument()
    directory = args["d"][0]
    file_list = walk_path(directory)

    #set up multiprocessing
    pool_size = min(multiprocessing.cpu_count(), 4)
    pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=10000)

    files = np.array_split(file_list, pool_size*2)

    # map
    pool_outputs = pool.map(add_lyrics, files)

    # join
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks

    bhUtilties.timeItEnd(1)
    # set_lyrics(file)
    # print get_tag(file)
    print "End Main"

