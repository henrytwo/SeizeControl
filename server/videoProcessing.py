from math import *
from pytube import YouTube
import os
import cv2
import numpy
from matplotlib import pyplot








class video:
    def __init__(self, url):
        self.url = url
        self.vid = 0
        self.width = 0
        self.height = 0
        self.getVid()
        self.frameArray = []
        self.frameCount = len(self.frameArray)
        self.getFrames()
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
        for i in range(10): #Go through all vid frames
            img = cv2.imread('ex.jpg', 0) #Put frame in here
            edges = cv2.Canny(img, 1, 500)
            self.frameArray.append(edges)


    def colourDist(self, col1, col2):
        return sqrt((col2[0] - col1[0])**2 + (col2[1] - col1[1])**2 + (col2[2] - col1[2])**2)

    #takes black and white cv edge frame and finds stripe patterns
    def stripeVal(self, Eframe):
        lineList = [[[0, 0] for j in range(80)] for i in range(45)]
        for i in range(0, self.height, self.height//45):
            for j in range(0, self.width, self.width//80):
                n = 0
                points = []
                for k in range(self.height//80):
                    for m in range(self.width//45):
                        if Eframe[i*self.height//45+k][j*self.width//80+m] == (255, 255, 255):
                            n += 1
                            points.append((i*self.height//45+k, j*self.width//80+m))
                if len(points) != 0:
                    sumx = sum(a[0] for a in points)
                    sumy = sum(a[1] for a in points)
                    sumxy = sum(a[0]*a[1] for a in points)
                    sumxx = sum(a[0]**2 for a in points)
                    sumyy = sum(a[1]**2 for a in points)
                    correlation = (n*sumxy-sumx*sumy)/sqrt((n*sumxx-sumx**2)*(n*sumyy-sumy**2))
                    slope = (sumxy - ((sumx*sumy)/n))/(sumxx - (sumx**2)/n)
                    if correlation > 0.9:
                        lineList[i][j] = [correlation, slope]
                    else:
                        lineList[i][j] = None
                else:
                    lineList[i][j] = None
        score = 0
        for i in lineList:
            for j in i:
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