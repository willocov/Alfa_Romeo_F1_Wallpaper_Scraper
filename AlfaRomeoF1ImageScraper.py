# Alfa Romeo F1 Wallpaper Image Scraper
# Created by William Covington
# Last Updated: 2022-11-19
# This script is used to download wallpaper images from Alfa Romeo's F1 website.
# These wallpapers are created as promotion for each race weekend.

# Images will be saved to the same directory as this file by default.
# An optional local or absolute filepath may be passed as a parameter
# The directory will be created if it does not exist.

# Usage: python FerrariImageScraper.py [optional local or absolute path]
# Note: Make sure to include a '\' at the end, or it's parent directory will be used, might fix later.

# Samples
# Same directory as file: python AlfaRomeoF1ImageScraper.py
# Local Path:  python AlfaRomeoF1ImageScraper.py output\
# Absolute Path: python AlfaRomeoF1ImageScraper.py C:\Users\pythonTests\Downloads\

import sys
import os
import requests
import urllib
from bs4 import BeautifulSoup
from pathlib import Path

# These variables are derived from HTML elements on Alfa Romeos's website and may change.
# ===================================================================================
# URL of the webpage containing all the wallpapers
WebPageURL = "https://www.sauber-group.com/motorsport/formula-1/gallery/getcloser-wallpapers/"
# Class name of the HTML element containing the image
WallpaperImageClassName = "ResponsiveImage--image"''
# ====================================================================================

if __name__ == '__main__':
    # Check if an output filepath was passed as parameter
    if len(sys.argv) > 1:
        # Filepath was passed, create a directory for it if necessary, then verify it exists.
        localOutputDirectory = sys.argv[1]
        Path(localOutputDirectory).mkdir(parents=True, exist_ok=True)
        isDirectory = os.path.isdir(localOutputDirectory)
        if isDirectory:
            # Directory exists, good to proceed
            print("Directory is good")
        else:
            # Failed to create directory, exit
            print("Directory is bad")
            quit()
    else:
        # No output filepath was passed as parameter, use same directory as this file
        localOutputDirectory = ""

    # Get the HTML data from Alfa Romeo's web page

    print("Getting HTML data from Alfa Romeo's web page")
    page = requests.get(WebPageURL)
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the URLs for each race's web page, adds URLs to a list
    print("Scraping Alfa Romeo's web page for images")
    urlList = []
    job_elements = soup.find_all("img", class_=WallpaperImageClassName)
    for job_element in job_elements:
        src_url = job_element["src"]
        src_url = src_url.replace("-5x9", "")
        print("Found Image: " + src_url)
        urlList.append(src_url)

    # Remove any duplicates and print results
    print("Removing Duplicate Image URLs")
    urlList = [*set(urlList)]
    print("Number of Image URLS Found: " + str(len(urlList)))

    # Download images, each image has same name with an incremented number
    print("Downloading Images")
    filenameCounter = 1  # Used to add a number to the end of each filename (e.g. ferrari_01.png)
    for image in urlList:
        try:
            urllib.request.urlretrieve(image, localOutputDirectory + f'AlfaRomeo_0{str(filenameCounter)}.png')
            print("Downloaded Image: " + image)
            filenameCounter += 1
        except Exception as e:
            print("Error: Failed to download image: " + image + " " + str(e))

    print("Number of Images Downloaded: " + str(filenameCounter - 1))