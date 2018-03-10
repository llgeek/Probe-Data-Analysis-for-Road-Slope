"""
@author: Linlin Chen
        lchen96@hawk.iit.edu 

This is the defined class LinkData 
used to store each link's info, including refID, nonrefID, direction, refInfo, nonrefInfo, shapeInfo and slopeInfo
"""

from geopy.distance import great_circle as distance
from geopy.point import Point
from math import radians, degrees, sin, cos, tan, asin, acos, atan2, sqrt, pi

class LinkData(object):
    def __init__(self, refID, nonrefID, direction, refInfo, nonrefInfo, shapeInfo, slopeInfo):
        """
        type refID: str, identifier for reference
        type nonrefID: str, identifier for nonreference
        type direction: str, indicate direction from refnode or towards refnode
        type refInfo: tuple, (latitute, longitute, altitute)
        type nonrefInfo: tuple, (latitute, longitute, altitute)
        type shapeInfo: list of tuples, each element is (latitute, longitute, altitute) for each shape node, None if no shape nodes
        type slopeInfo: list of tuples, (distance, slope)
        """

        self.refID = refID
        self.nonrefID = nonrefID
        self.direction = direction
        self.refInfo = refInfo
        self.nonrefInfo = nonrefInfo
        self.shapeInfo = shapeInfo
        self.slopeInfo = slopeInfo

        self.avgslope = self.setavgslope()

    def setavgslope(self):
        """
        average all the slope values for one link
        """
        if not self.slopeInfo:
            return None
        slopesum, slopenum = 0.0, 0
        for slope in self.slopeInfo:
            if len(slope) == 2:
                slopesum += slope[0]
                slopenum += 1
        return slopesum / slopenum


    def calcdistanceFromRef(self, pointlist):
        """
        pointlist type: list of tuples
        each tuple stores the longitute, latitute and altitute of the each probe point
        return distance from ref node for each peobe point
        """
        distlist = [distance(self.refInfo, point).meters for point in pointlist]
        return distlist

    def calcavgdistance(self, pointlist):
        """
        give the point list of each probe data, calculate the distance to reference node for each point
        """
        distlist = self.calcdistanceFromRef(pointlist)
        return sum(distlist) / len(distlist)


    def calcdistanceFromLink(self, pointlist):
        """
        give the point list of each probe data, calculate the perpendicular distance to the link for each point
        """
        distlist = [self.perpendicularDist(self.refInfo, self.nonrefInfo, point) for point in pointlist]
        return distlist


    def perpendicularDist(self, endpoint1, endpoint2, point):
        """
        Helper method for calcdistanceFromLink, calculate the perpendicular distance of point to the line 
        by two end point, endpoint1 and endpoint2
        """
        point1_lat, point1_lon = radians(endpoint1[0]), radians(endpoint1[1])
        point2_lat, point2_lon = radians(endpoint2[0]), radians(endpoint2[1])
        point_lat, point_lon = radians(point[0]), radians(point[1])

        #dist1p = sqrt((point_lat - point1_lat)**2 + (point_lon - point1_lon)**2)
        dist1p = distance(point, endpoint1).meters
        #dist12 = sqrt((point2_lat - point1_lat)**2 + (point2_lon - point1_lon)**2)
        dist12 = distance(endpoint1, endpoint2).meters

        if dist1p == 0 or dist12 == 0:
            return 0
        return sin(acos((point_lat - point1_lat)*(point2_lat -point1_lat) + (point_lon - point1_lon)*(point2_lon - point1_lon))/(dist12*dist1p))*dist1p*1609.34


    # def perpendicularDist(self, endpoint1, endpoint2, point):
    #     point1_lat, point1_lon = radians(endpoint1[0]), radians(endpoint1[1])
    #     point2_lat, point2_lon = radians(endpoint2[0]), radians(endpoint2[1])
    #     delta_lon = point2_lon - point1_lon
    #     point2_x = cos(point2_lat) * cos(delta_lon)
    #     point2_y = cos(point2_lat) * sin(delta_lon)
    #     interpoint_lat = atan2(sin(point1_lat) + sin(point2_lat), sqrt((cos(point1_lat) + point2_x)**2 + point2_y**2))
    #     interpoint_lon = point1_lon + atan2(point2_y, cos(point1_lat) + point2_x)
    #     # Normalise
    #     interpoint_lon = (interpoint_lon + 3*pi) % (2*pi) - pi
    #     return distance((interpoint_lat, interpoint_lon), point).meters




