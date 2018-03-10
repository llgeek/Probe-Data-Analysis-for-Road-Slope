import math
from geopy.distance import great_circle as distance

class ProbeData(object):
    def __init__(self, sampleID, duration, shapeInfo, geohashtag, candidatelist):
        self.sampleID = sampleID
        self.duration = duration
        self.shapeInfo = shapeInfo
        self.geohashtag = geohashtag
        self.candidatelist = candidatelist

        # following are mapping attributes
        self.mappingsucessful = False
        self.maplinkID = -1
        self.distFromRef = []
        self.distFromLink = []
        self.slpoe = []


    def setMapInfo(self, linkID, distFromRef, distFromLink):
        """
        set the mapping information
        """
        self.mappingsucessful = True
        self.maplinkID = linkID
        self.distFromRef = distFromRef[:]
        self.distFromLink = distFromLink[:]

    def setSlope(self, refnodeInfo):
        """
        calculate the slope for each probe data point
        """
        prev = refnodeInfo
        for cur in self.shapeInfo:
            self.slpoe.append(self.slopeDegree(prev, cur))
            prev = cur

    def slopeDegree(self, node1, node2):
        """
        helper method for setSlope, it will use two nodes, and then calculate the slope value
        """
        if len(node1) != 3 or len(node2) != 3 or distance(node1, node2).meters == 0:
            return 0
        # try:
        return math.degrees(math.atan((node2[2]-node1[2])/distance(node1, node2).meters ))
        # except ValueError:
        #     #print("Value Error occured for node1: {}, node2: {}".format(node1, node2))
        #     sinval = (node2[2]-node1[2])/distance(node1, node2).meters
        #     sinval = -1 if sinval < -1 else 1 if sinval > 1 else sinval
        #     return math.degrees(math.asin(sinval))
    

    # def caldistFromLink(self, refshapeinfo)


class ProbeAdditionalInfo(object):
    """
    Stores the irrelevant info, for fast lookup when writing result back to csv
    additional information includes: dateTime, speed, heading
    """
    def __init__(self, dateTimelist, sourceCodelist, speedlist, headinglist):
        self.dateTimelist = dateTimelist
        self.sourceCodelist = sourceCodelist
        self.speedlist = speedlist
        self.headinglist = headinglist


