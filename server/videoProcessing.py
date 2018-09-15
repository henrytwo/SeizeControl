from math import *
from pytube import YouTube
import os
import cv2
import numpy
from matplotlib import pyplot

img = cv2.imread('messi5.jpg',0)
edges = cv2.Canny(img,100,200)

img = cv2.imread('dave.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,200)
for rho,theta in lines[0]:
    a = numpy.cos(theta)
    b = numpy.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite('houghlines3.jpg',img)

plt.show()

class video:
    def __init__(self, url):
        self.url = url
        self.getVid()
        self.vid = 0
        self.width = 0
        self.height = 0
        self.frameArray = []
        self.frameCount = len(self.frameArray)
        self.maxDist = 443.405007
        self.scores = []

    #downloads vid to be processed
    def getVid(self):


        YouTube(self.url).streams.last().download()

        self.vid = 0
        self.width = 0
        self.height = 0

    #Takes video and makes frame array
    def getFrames(self):
        self.frameArray = []
        self.frameCount = len(self.frameArray)

    def colourDist(self, col1, col2):
        return sqrt((col2[0] - col1[0])**2 + (col2[1] - col1[1])**2 + (col2[2] - col1[2])**2)


    def stripeVal(self, Aframe):
        pass

    def checkerVal(self, Aframe):
        pass

    #Takes frame and gets adjacent square differences
    def adjacencyContrast(self, frame):
        adjFrame = [[0 for i in range(self.width - (j%2))] for j in range(self.height*2-1)]
        for i in range(0, self.height, 2):
            for j in range((2*i)%5, self.width, 2):
                if i < self.height-1:
                    adjFrame[i][j] = self.colourDist(frame[i][j], frame[i+1][j])
                if i > 0:
                    adjFrame[i-1][j] = self.colourDist(frame[i][j], frame[i-1][j])
                if j < self.width-1:
                    adjFrame[i][j] = self.colourDist(frame[i][j], frame[i][j+1])
                if j > 0:
                    adjFrame[i][j-1] = self.colourDist(frame[i][j], frame[i][j-1])
        return self.stripeVal(adjFrame) + self.checkerVal(adjFrame)

    #Gets basic contrast of Cframe (0 to 100)
    def totContrast(self, Cframe):
        s = 0
        for col in Cframe:
            s += sum(col/(self.width*self.maxDist))
        s *= 100/self.height
        return s

    #Sends fixed score to server
    def sendScore(self, index):
        start = max(0, index-9)
        return sum(self.scores[start, index+1])/(index-start+1)

    #Goes through all contrast frames and generates scores, "main" of the class
    def getScores(self):
        for i in range(self.frameCount - 1):
            score = self.getContrast(self.frameArray[i], self.frameArray[i+1])
            self.scores.append(score)
            self.sendScore(i)

    #Creates the contrast frame between two frames and gets epilepsy value
    def getContrast(self, frame1, frame2):
        contrastFrame = [[0 for i in range(self.width)]for j in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                contrastFrame[i][j] = self.colourDist(frame1[i][j], frame2[i][j])
        return (self.getContrastScore(contrastFrame) + self.adjacencyContrast(frame1))/2

    #Code to delete the video file downloaded
    def die(self):
        os.remove("ChangedFile.csv")




test = video("https://www.youtube.com/watch?v=fhiHqz8Ur24")