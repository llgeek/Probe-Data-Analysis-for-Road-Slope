"""
author: Linlin Chen
        lchen96@hawk.iit.edu

This module is used to process the linkdata 

For the initialization, input the source path, source file name and target path(to put the output file)
The loadData will handle all the process, it will return the geohash map(with precision 7 and precision 8) and the link infomation,
which is represented as ProbeData class
"""


import os
import numpy as np
import pickle
import csv
from collections import defaultdict
from LinkData import LinkData
import geohash

class LinkDataProcess(object):
    def __init__(self, sourcepath, sourcefilename, tgtpath):
        """ 
        sourcepath type: str 
        sourcefilename type: str 
        tgtpath type: str 
        """
        self.sourcepath = sourcepath
        self.sourcefilename = sourcefilename
        self.tgtpath = tgtpath
        self.sourcefile = os.path.join(self.sourcepath, self.sourcefilename)

        self.geohashmap7precfilename = 'Link_geohash_7_prec.pickle'
        self.geohash7precfile = os.path.join(self.tgtpath, self.geohashmap7precfilename)
        self.geohashmap8precfilename = 'Link_geohash_8_prec.pickle'
        self.geohash8precfile = os.path.join(self.tgtpath, self.geohashmap8precfilename)

        self.linkinfofilename = 'linkData.pickle'
        self.linkinfofile = os.path.join(self.tgtpath, self.linkinfofilename)


    def loadData(self):
        """
        load the data from file, save the processed content with pickle

        return:
            geohashmap7prec: geohash with precision 7, dic type
            geohashmap8prec: geohash with precision 8, dict type
            linkInfo: linkinfo, ProbeData type

        """

        print("Load link data now...")
        if os.path.exists(self.geohash7precfile) and os.path.exists(self.geohash8precfile) and os.path.exists(self.linkinfofile):
            try:
                geohashmap7prec = self.loadFilewithPickle(self.geohash7precfile)
                geohashmap8prec = self.loadFilewithPickle(self.geohash8precfile)
                linkInfo = self.loadFilewithPickle(self.linkinfofile)
                return geohashmap7prec, geohashmap8prec, linkInfo
            except RuntimeError:
                print("\tFiles already exist, but pickle load uncessfully!")
        
        geohashmap7prec = defaultdict(list)        #store 7 length geohash, precision <= 153m * 153m
        geohashmap8prec = defaultdict(list)        #store 8 length geohash, precision <= 38.2 * 19.1
        linkInfo = defaultdict()
        with open(self.sourcefile, 'r') as linkfile:
            #linkPVID, refNodeID, nrefNodeID, directionOfTravel, shapeInfo, curvatureInfo, slopeInfo = np.loadtxt(linkfile, dtype =str, delimiter = ',', usecols = (), unpack=True)
            linkreader = csv.reader(linkfile, delimiter = ',')
            for line in linkreader:
                linkPVID, refNodeId, nrefNodeID, directionOfTravel, shapeInfo, slopeInfo = \
                    line[0], line[1], line[2], line[5], line[14], line[16]
                #check whether shapeInfo is empty
                # We only consider link with valid latitute and longitute information
                if shapeInfo and len(shapeInfo.split('|')) >= 2:
                    shapeInfo = shapeInfo.split('|')
                    refInfo = tuple(float(val) for val in shapeInfo[0].split('/') if val)
                    nonrefInfo = tuple(float(val) for val in shapeInfo[-1].split('/') if val)
                    # refnode and nonref node must at least have longitute and latitute info, otherwise skip
                    if len(refInfo) < 2 or len(nonrefInfo) < 2:
                        continue
                    shapenodeInfo = [tuple(float(val) for val in info.split('/') if val) for info in shapeInfo[1:-1]]
                    slopeinfo = None if not slopeInfo else [tuple(float(val) for val in info.split('/') if val) for info in slopeInfo.split('|')]
                    linkInfo[linkPVID] = LinkData(refNodeId, nrefNodeID, directionOfTravel, 
                        refInfo, nonrefInfo, shapenodeInfo, slopeinfo)
                    
                    #geohashmap7prec[geohash.encode(*refInfo[:2], precision=7)] = geohashmap7prec.get(geohash.encode(*refInfo[:2], precision=7), set()).add(linkPVID)
                    geohashmap7prec[geohash.encode(*refInfo[:2], precision=7)].append(linkPVID)
                    #geohashmap8prec[geohash.encode(*refInfo[:2], precision=8)] = geohashmap8prec.get(geohash.encode(*refInfo[:2], precision=8), set()).add(linkPVID)
                    geohashmap8prec[geohash.encode(*refInfo[:2], precision=8)].append(linkPVID)

        try:
            self.dumpFilewithPickle(self.geohash7precfile, geohashmap7prec)
            self.dumpFilewithPickle(self.geohash8precfile, geohashmap8prec)
            self.dumpFilewithPickle(self.linkinfofile, linkInfo)
        except RuntimeError:
            print("Cannot save files with pickle!")
        return geohashmap7prec, geohashmap8prec, linkInfo

    def loadFilewithPickle(self, file):
        """
        load data from file with pickle
        """
        with open(file, 'rb') as loadfile:
            return pickle.load(loadfile)


    def dumpFilewithPickle(self, file, content):
        """
        save object to file with pickle
        """
        with open(file, 'wb') as savefile:
            pickle.dump(content, savefile)



# lps = LinkDataProcess('./probe_data_map_matching/', 'Partition6467LinkData.csv', './probe_data_map_matching/')
# geohashmap7prec, geohashmap8prec, linkInfo = lps.loadData()

# print(len(geohashmap7prec), len(geohashmap8prec), len(linkInfo))

# import itertools
# for k, v in itertools.islice(geohashmap7prec.items(), 0, 10):
#     print(k, v)
# for k, v in itertools.islice(geohashmap8prec.items(), 0, 10):
#     print(k,v)
# for k, v in itertools.islice(linkInfo.items(), 0, 10):
#     print(k, v.refID, v.slopeInfo)
