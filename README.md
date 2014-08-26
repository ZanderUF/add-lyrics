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

    python naivebayes.py -d directory

where directory is a directory of the format:

    directory
        +-category1
        |   +files in category1
        |   +...
        |
        +cateogry2
        |   +files in category2
        |   +...
        |
        +...

This is designed to match the dataset included with this git, and available at
http://www.cs.cornell.edu/people/Pabo/movie-review-data/ . Please note that the categories are determined with each run,
and are not limited to the 'pos' and 'neg' categories in this example data set.

##CURRENT IMPLEMENTATION-Optimization
**********************************
In order to maximize average correct identification, there are a few modifications on the general Naive-Bayes format.
In particular, some words are re-weighted in bhUtilities.splitAndCleanString(), and known negative and positive words
are added in naivebayes.train().

Additionally, I've done some work to reduce run time. In my implementation, reading files was a major bottleneck, so
I simply pickle a dictionary containing all words contained in every document. This is not realistic for larger
databases (and you should probably look into mmap or just reading documents when they are needed).

Finally, all categories recieve equal probability in this implementation. This can be changed by modifying:

    P_c = float(len(catList))**-1 #equal weighting

##THANK YOU's
**********************************
This base project was created as a project submission for the Summer 2014 section of MSAN 593, taught at the University
of San Francisco by Yannet Interian. I would like to thank her and the faculty for their support and guidance.

As a side note, I've written all code in this package from scratch (excluding imports, obviously). As such, I am able
to make it available under the MIT License.