"""
@author: Linlin Chen
    lchen96@hawk.iit.edu 

This module is used to process the probe data
Store the intermediate results and get the candidate links for each probe data
"""

import os
import numpy as np
import pickle
import csv
import geohash
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from ProbeData import ProbeData, ProbeAdditionalInfo
from LinkData import LinkData

from LinkDataProcess import LinkDataProcess


class ProbeDataProcess(object):
    def __init__(self, sourcepath, sourcefilename, tgtpath, geohash7prec_link, geohash8prec_link):
        self.sourcepath = sourcepath
        self.tgtpath = tgtpath

        self.sourcefilename = sourcefilename
        self.sourcefile = os.path.join(self.sourcepath, self.sourcefilename)

        # self.datefilename = 'probeDateTime.pckl'
        # self.datefile = os.path.join(self.tgtpath, self.datefilename)
        
        # self.geohash7precfilename = 'Probe_geohash_7_prec.pickle'
        # self.geohash8precfilename = 'Probe_geohash_8_prec.pickle'
        # self.geohash7precfile = os.path.join(self.tgtpath, self.geohash7precfilename)
        # self.geohash8precfile = os.path.join(self.tgtpath, self.geohash8precfilename)

        self.probeInfofilename = 'probeData.pickle'
        self.probeInfofile = os.path.join(self.tgtpath, self.probeInfofilename)

        self.addiInfofilename = 'probeDataAddiInfo.pickle'
        self.addiInfofile = os.path.join(self.tgtpath, self.addiInfofilename)

        self.geohash7prec_link = geohash7prec_link
        self.geohash8prec_link = geohash8prec_link
        

    def loadData(self):
        """
        load data from probe data file
        return type: probeInfo: list, a list of ProbeData elements, store necessary information for each probe data 
                    addiInfo: dict, a dictionary storing the additional information needed for writing results back, no use for probe data mapping
        """

        print('\n\nLoad probe data now...')
        if os.path.exists(self.probeInfofile) and os.path.exists(self.addiInfofile):
            try:
                probeInfo = self.loadFilewithPickle(self.probeInfofile)
                addiInfo = self.loadFilewithPickle(self.addiInfofile)
                return probeInfo, addiInfo
            except RuntimeError:
                print("\tFiles already exist, but pickle load uncessfully!")

        probeInfo = []
        #addiInfo = dict()
        addiInfo = []

        with open(self.sourcefile, 'r') as probefile:
            probereader = csv.reader(probefile, delimiter = ',')

            shapeInfo = []

            datetimelist = []
            sourcecodelist = []
            speedlist = []
            headinglist = []

            previd = -1
            prevstime, preetime = datetime.now(), datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
            for line in probereader:
                if len(line) != 8:
                    continue
                sampleID, dateTime, sourcecode, latitude, longitude, altitude, speed, heading = line
                if sampleID != previd:
                    if previd != -1:
                        geohashtag, candidatelist = self.calcCandidateLinks(shapeInfo)
                        if geohashtag:
                            duration = (datetime.strptime(preetime, '%m/%d/%Y %I:%M:%S %p') - prevstime).total_seconds()
                            #addiInfo[sampleID] = ProbeAdditionalInfo(datetimelist, sourcecodelist, speedlist, headinglist)
                            addiInfo.append(ProbeAdditionalInfo(datetimelist, sourcecodelist, speedlist, headinglist))
                            probeInfo.append(ProbeData(previd, duration, shapeInfo, geohashtag, candidatelist))
                    
                    prevstime = datetime.strptime(dateTime, '%m/%d/%Y %I:%M:%S %p')
                    previd = sampleID
                    shapeInfo = []  
                    
                    datetimelist = []
                    sourcecodelist = []
                    speedlist = []
                    headinglist = []


                shapeInfo.append(tuple((float(latitude), float(longitude), float(altitude))))
                datetimelist.append(dateTime)
                sourcecodelist.append(sourcecode)
                speedlist.append(speed)
                headinglist.append(heading)
                preetime = dateTime

        try:
            self.dumpFilewithPickle(self.probeInfofile, probeInfo)
            self.dumpFilewithPickle(self.addiInfofile, addiInfo)
        except RuntimeError:
            print("Cannot save files with pickle!")

        return probeInfo, addiInfo



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


    def calcCandidateLinks(self, shapeInfo):
        """
        using geohash to filter the candidate links
        firstly we apply geohash with precision 8, if there exists more than 5 links then return that as geohashtag
        else we apply geohash with precision 7, then check if there exists at least one link, then return that as geohash
        otherwise, return None, None

        rtype: geohashtag: type str, as the geohash value for this probe data
                linksIDs: type list, a list of linkPVIDs of candidate links
        """
        geohashtags = [geohash.encode(*shape[:2], precision=8) for shape in shapeInfo]
        for geohashtag, _ in Counter(geohashtags).most_common():
            if geohashtag in self.geohash8prec_link and len(self.geohash8prec_link[geohashtag]) >= 5:
                return geohashtag, self.geohash8prec_link[geohashtag]
        geohashtags = [geohash.encode(*shape[:2], precision=7) for shape in shapeInfo]
        for geohashtag, _ in Counter(geohashtags).most_common():
            if geohashtag in self.geohash7prec_link:
                return geohashtag, self.geohash7prec_link[geohashtag]
        return None, None


# lps = LinkDataProcess('./probe_data_map_matching/', 'Partition6467LinkData.csv', './probe_data_map_matching/')
# geohashmap7prec, geohashmap8prec, linkInfo = lps.loadData()
# print(len(geohashmap7prec), len(geohashmap8prec), len(linkInfo))


# pds = ProbeDataProcess('probe_data_map_matching/', 'Partition6467ProbePoints.csv', 'probe_data_map_matching/', geohashmap7prec, geohashmap8prec)
# probeInfo, addiInfo = pds.loadData()
# print(len(probeInfo), len(addiInfo))
