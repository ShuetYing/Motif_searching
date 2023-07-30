#!/usr/bin/python3

import sys

while True:
        try:
                window_size = str(int(input("Please specify the window size (window of comparison) used for plotting:\n")))
                print("window size = ", window_size)
                break
        except ValueError:
                print("Please enter an integer!")

cmd = "plotcon MSA.fa -winsize " + window_size + " -graph png"   # plot the conservation plot with specified window size
os.system(cmd)

import PIL
from PIL import Image
img = Image.open('plotcon.1.png')
img.show()

print("Hmmm, it might take a while to load the image, please be patient...")
