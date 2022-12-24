# viscrape
A Python script to know when a website got updated by taking screenshots of it.

Supports:
- Webpage screenshots (with cropping that uses a GUI)
- Web browser extensions (you may use an adblocker)
- Cookies loading (to scrape webpages that require authentication)
- Customization arguments (zoom, interval seconds)

&nbsp;
## Requirements
- [Python 3](https://www.python.org/downloads/) with pip.

- Firstly install all the libraries required to run the program. They are stored in "requirements.txt".<br>
To install them run "`pip install -r requirements.txt`".

- [ungoogled-chromium](https://ungoogled-software.github.io/ungoogled-chromium-binaries/releases/windows/64bit/). Download the last version for windows 64-bit (not the installer).<br>
Normal chromium or even chrome should be fine, but i've still not tested my program with them.<br>
Paste all the files of the "chrome.exe" folder into the "browser" folder.

- [ChromeDriver](https://chromedriver.chromium.org/downloads). Download it the same version as ungoogled chromium (as of now it's v108), then paste it in the "browser" folder.

- You're basically done, but you CAN and SHOULD download an adBlocker for webpage consistency purposes.<br>
Use [this website](https://standaloneinstaller.com/online-tools/crx-downloader) to download uBlock Origin or similar adblockers and paste it into the "extensions" folder (as .crx file).

&nbsp;
## Arguments

| Command       | Shorthand | Example                      | Description
|:-:            |:-:        | :-:                          |:-
| --crop        | -c        | `-c 20,10,50,60`             | Screenshot crop coordinates. Default is don't crop.<br>In case of "`-c gui`", a GUI will appear to let the user decide where to crop.
| --zoom        | -z        | `-z 75`                      | Webpage zoom percent. Default is 100.
| --interval    | -i        | `-i 10`                      | Interval seconds between scrapes. Default is 5.
| --cookies     | -C        | `-C "path/to/cookies.json"`  | Path where to get cookies. Default is in the same folder of viscrape.py.<br>In case of "`-C .`", invalid path or cookies not found, no cookies will be used.<br>In case of "`-c gui`", a browser window will open to let you do stuff like logging in and save the cookies.
| --screenshots | -s        | `-s "path/for/screenshots/"` | Path where to store screenshots. Default is in "screenshots/".<br>In case of "`-s .`" or invalid path, no screenshots will be saved.
|               |           | `https://any.website.com/`   | Webpage to scrape. Parameter required.

&nbsp;
### Examples
```
py viscrape.py -c 620,454,893,553 -C gui -z 100 https://www.youtube.com/@YouTube
```
```
py viscrape.py -c gui -i 20 -s D:/Screenshots/ https://www.amazon.it/dp/B08WHML7GL/
```
