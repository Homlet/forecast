f o r e c a s t
===============

forecast can predict when your location will next be photographed by NASA's
satellites. forecast is an easy to use, command line tool, with only a
couple of prerequisites:

 - Python 2.7
 - [geopy](https://github.com/geopy/geopy)
 - [nasa-api-wrapper](https://github.com/brendanv/nasa-api)

Usage is simple: if you have a coordinate pair (latitude and longitude),
execute the file with the option --coord, followed by the coordinate.

**e.g.:** `python forecast.py --coord 51.511407 -0.116043`

If you don't have a coordinate pair, forecast can generate one for you,
from an address. Simply execute with --address, followed by the address.

**e.g.:** `python forecast.py --address Homerton College, Cambridge, CB2 8PH`

forecast will return a single YYYY-MM-DD hh:mm:ss datetime: its best prediction for
when then next photo will be taken.  
*Be prepared!*

forecast was developed in less than 24 hours as an entry for the 2015
HackKings hackathon at King's College London.
