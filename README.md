# Facebook Message Export Parser

Facebook has a feature that allows users to download a copy of their data as a zip archive containing htm files with their data. The aim of this parser is to take this archive and to extract a user's Facebook Messages from it; to transfer them into a more useful format, as well as performing some analysis to produce interesting data.


#### Running the Code
The Facebook Export can be downloaded from  the [Facebook Settings](https://www.facebook.com/settings) menu. 

Run "python fb_parser.py" with the 'messages.htm' file in the same directory to export to JSON as proof of concept.

#### Dependencies
The code is written in Python 3+. The parser uses [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) to do the bulk of the capture from the htm file.

[Anaconda Python](https://store.continuum.io/cshop/anaconda/) for scientific computing is a simple and easy way to install all the dependencies for the code, alongside many other useful libraries. It can be downloaded [here](http://continuum.io/downloads).
