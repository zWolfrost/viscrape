import getopt, time, sys, json, os, numpy, cv2

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

from PIL import Image, ImageChops
from io import BytesIO

from datetime import datetime


def saveImage(image, path):
   imgbytes = BytesIO()
   image.save(imgbytes, format="png")

   if (os.path.isdir(path) == False):
      os.makedirs(path)

   path += datetime.today().strftime("%H.%M.%S")

   if (os.path.exists(f"{path}.png")):
      filenum = 0
      while True:
         filenum += 1
         if (os.path.exists(f"{path} ({str(filenum)}).png") == False):
            path = f"{path} ({str(filenum)})"
            break

   path += ".png"

   with open(path, "wb") as file:
      path = file.name
      file.write(imgbytes.getvalue())


def imagesAreIdentical(img1, img2):
   cv2img1 = cv2.cvtColor(numpy.array(img1), cv2.COLOR_RGB2BGR)
   cv2img2 = cv2.cvtColor(numpy.array(img2), cv2.COLOR_RGB2BGR)

   return numpy.any(cv2.subtract(cv2img1, cv2img2)) == False


def getPageScreenshot(driver, cropPos=None):

   screenshot = driver.get_screenshot_as_png()
   screenshot = Image.open(BytesIO(screenshot)).crop(cropPos)

   return screenshot




####
## Get cli arguments
####

#sys.argv[1:]
#test = "-c 620,454,893,553 -C gui https://www.youtube.com/@YouTube".split()
ARGS = getopt.getopt(sys.argv[1:], "c:z:i:C:s:", ["crop=", "zoom=", "interval=", "cookies=", "screenshots="])

try:
   WEBPAGE = ARGS[1][0]
except Exception:
   print("No webpage was given. Please retry.")
   quit()

CROP = None
ZOOM = "100"
INTERVALSECS = 5
COOKIESPATH = "./cookies.json"
SCREENSHOTPATH = f"./screenshots/{datetime.today().strftime('%y.%m.%d %H.%M.%S')}/"

try:
   for opt, arg in ARGS[0]:
      if opt in ["-c", "--crop"]:
         if (arg == "gui"): CROP = arg
         else: CROP = json.loads(f"[{arg}]")
      elif opt in ["-z", "--zoom"]: ZOOM = arg
      elif opt in ["-i", "--interval"]: INTERVALSECS = int(arg)
      elif opt in ["-C", "--cookies"]: COOKIESPATH = arg
      elif opt in ["-s", "--screenshots"]:
         if os.access(os.path.dirname(arg) or os.getcwd(), os.W_OK): SCREENSHOTPATH = arg
         else: SCREENSHOTPATH = None
except Exception as e:
   print("Arguments contain syntax errors. Please retry.")
   quit()


####
## Create driver
####

BROWSER_EXE_PATH = "./browser/chrome.exe"
BROWSER_DRIVER_PATH = "./browser/chromedriver.exe"
EXTENSIONS_PATH = "./extensions/"

options = Options()

#options.add_argument("--incognito")
options.add_argument("--headless=chrome")
options.add_argument("--window-size=2560,1440")
options.add_argument("--disable-partial-raster")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.binary_location = BROWSER_EXE_PATH

for extname in os.listdir(EXTENSIONS_PATH):
   options.add_extension(EXTENSIONS_PATH + extname)

driver = Chrome(service=Service(executable_path=BROWSER_DRIVER_PATH), options=options)

try:
   driver.get(WEBPAGE)
except:
   print("Webpage URL is invalid. Please retry.")
   quit()


####
## Get cookies and apply them
####

if (COOKIESPATH == "gui"):
   from libraries.setup_cookies import getCookiesGUI, saveCookies

   COOKIESPATH = "./cookies.json"

   saveCookies(getCookiesGUI(BROWSER_EXE_PATH, BROWSER_DRIVER_PATH, WEBPAGE), COOKIESPATH)

cookies = None

try:
   with open(COOKIESPATH, "r") as cookiesJSON:
      cookies = json.load(cookiesJSON)
except Exception:
   pass

if (cookies is None):
   print("No cookies found, loading page...")
else:
   errorCookies = 0

   for cookie in cookies:
      try:
         driver.add_cookie(cookie)
      except Exception:
         errorCookies += 1

   print(f"Successfully added {len(cookies) - errorCookies} cookies of {len(cookies)}, reloading page...")

   driver.get(WEBPAGE)


####
## Make first Fetch
####

driver.get(WEBPAGE)
driver.execute_script(f"document.body.style.zoom='{ZOOM}%'")
if (INTERVALSECS > 0): time.sleep(INTERVALSECS)


####
## Get crop coordinates
####

if (CROP == "gui"):
   from libraries.get_coords_gui import getCoordsGUI

   image = getPageScreenshot(driver)

   print(f"Select your crop coordinates on the created window.")

   CROP = getCoordsGUI(image)

   print(f"Coordinates confirmed! -> ({str(CROP[0])}, {str(CROP[1])}); ({str(CROP[2])}, {str(CROP[3])})")


####
## Make first screenshot
####

begScreen = getPageScreenshot(driver, CROP)

if (SCREENSHOTPATH is not None): saveImage(begScreen, SCREENSHOTPATH)

print(f'First fetch made! "{WEBPAGE}" will be updated every {INTERVALSECS} seconds')


####
## Fetch and screenshot until notice differences
####

updates = 1
errors = 0

while True:
   try:
      driver.get(WEBPAGE)
      driver.execute_script(f"document.body.style.zoom='{ZOOM}%'")
      if (INTERVALSECS > 0): time.sleep(INTERVALSECS)

      curScreen = getPageScreenshot(driver, CROP)

      updates += 1

      if (imagesAreIdentical(begScreen, curScreen)):
         print(f"No changes ({str(updates)} updates, {str(errors)} errors)", end="\r")
      else:
         print(f"CHANGES DETECTED! ({str(updates)} updates, {str(errors)} errors)", end="\a\n")

         if (SCREENSHOTPATH is not None): saveImage(curScreen, SCREENSHOTPATH)

         break

   except Exception:
      errors += 1


print(f"Closing drivers...")

driver.quit()