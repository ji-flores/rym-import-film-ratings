# rym-import-film-ratings

(Very) Work In Progess.

Simple Python tool for **import film ratings** (although it could easily be modified for all supported media types) **to a rateyourmusic.com profile**, **from a .csv** originally thought to be the one you get when exporting your film ratings from Letterboxd.

Automation using Selenium. Doesn't use headless browser for the moment. Also not sure how well it will hold up upon UI changes in rym. Oh well.

## TO DO

+ Fix: Sometimes it finds and rates a film that is not the specified on the .csv input file. Pretty much only a problem for little known films (in the context of western-centric communities like rym), which makes them not the first result on the search engine.
+ Pretty much the entire front end.
+ Headless browser.
