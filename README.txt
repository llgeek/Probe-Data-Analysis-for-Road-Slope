How to run the code:

*****************************************************
Please make sure the following environment is configured:

1. Python 3.5+
2. geopy
3. multiprocessing
4. pickle
5. geohash
6. csv


*****************************************************
To run the script, simply input the following commands in Terminal:

python3 ProbeMapMatching.py

For simplicity, I named the folder and file names the same as downloaded. So please make sure to put the probe and link data files in the folder named with 'probe_data_map_matching' in the current folder. The link data file name is 'Partition6167LinkData.csv'. The probe data file name is 'Partition6167ProbePoints.csv'




source files:
1. ProbeMapMatching.py:
	This is the main class to process the probe mapping, distance calculation and slope calculation and evaluation. Main function is also in this file.

2. ProbeDataProcess.py:
	This module is used to process the probe data. Store the intermediate results and get the candidate links for each probe data

3. ProbeData.py:
	This modlue is for the class ProbeData and ProbeAdditionalInfo, which will store informatio fo probe data points.

4. LinkDataProcess.py:
	This module is used to process the linkdata. For the initialization, input the source path, source file name and target path(to put the output file). The loadData will handle all the process, it will return the geohash map(with precision 7 and precision 8) and the link infomation, which is represented as ProbeData class

5. LinkData.py:
	This is the defined class LinkData, which is used to store each link's info, including refID, nonrefID, direction, refInfo, nonrefInfo, shapeInfo and slopeInfo.


All of my code files are detailedly commented. 




The output files are:

1. MatchedPoints.csv:
	This file stores the MatchedPoints Record, where the format is followed as required in readme-mapmatching.txt file, including:
		sampleID, dateTime, sourceCode, latitude, longitude, altitude, speed, heading, linkPVID, direction, distFromRef, distFromLink

2. MatchedPointsSlope.csv:
	This file stores the slope information for each probe link, and the corresponding surveyed slope information of the link data. 

To reduce the time complexity, I preprocess both the link data file and probe data file, so that probe mapping process won't repeat these proproessing again. I store the useful preprocessed results in the pickle files with pickle dump. The files include:

3. Link_geohash7_prec.pickle:
	This is the geohash with precission equals 7 of each link data. I use the reference node for the geohash.

4. Link_geohash8_prec.pickle:
	This is the geohash with precission equals 8 of each link data. I use the reference node for the geohash.

5. linkData.pickle:
	This is the processed link data information. It's a list of LinkData objects, so that each element is LinkData object. 

6. probeData.pickle:
	This is the processed probe data information. It's a list of ProbeData objects, so that each element is ProbeData object. 

7. probeDataAddiInfo.pickle:
	This is the prrocessed additional probe data information. These informaiton won't be used in the probe mapping stage, but is useful to store the mapped file. It's a list of ProbeAdditionalInfo objects.





