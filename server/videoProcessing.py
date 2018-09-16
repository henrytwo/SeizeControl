from math import *
from pytube import YouTube
import os
import cv2
import numpy
from matplotlib import pyplot








class video:
    def __init__(self, url):
        self.url = url
        self.maxDist = 443.405007
        self.scores = []
        self.vid = 1
        self.width = 1
        self.height = 1
        self.frameArray = []
        self.frameCount = len(self.frameArray)
        self.getFrames()


        #self.getScores()

    #downloads vid to be processed
    def getVid(self):
        YouTube(self.url).streams.last().download()
        self.vid = 1
        self.width = 1
        self.height = 1

    #Takes video and makes frame array
    def getFrames(self):
        self.frameArray = []


        counter = -1
        yt = YouTube(self.url)
        qualityList = ["360p", "144p", "240p", "480p", "720p"]
        bol = True
        edited = []
        while bol:
            if len(edited) == 0:
                counter += 1
            else:
                bol = False
            edited = yt.streams.filter(res=qualityList[counter], only_audio=False, mime_type="video/mp4").all()


        stream = yt.streams.filter(res=qualityList[counter], only_audio=False, mime_type="video/mp4").first()
        stream.download()
        print(qualityList[counter])

        cap = cv2.VideoCapture(yt.title + ".mp4")
        frameList = []
        start = False
        prevFrame = None
        ret, frame = cap.read()
        self.width, self.height = len(frame[0]), len(frame)
        frameCount = 0
        print(yt.streams.filter(res=qualityList[counter], only_audio=False, mime_type="video/mp4").first())
        FPS = 30
        while (cap.isOpened()):

            prevFrame = frame
            ret, frame = cap.read()
            if start and (frameCount % (FPS//4) == 0):
                score = self.getContrast(frame, prevFrame)
                self.scores.append(score)
                self.sendScore()
                try:
                    pass
                except:
                    pass
            start = True
            if ret:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

            frameCount += 1
        print(self.scores)
        #os.remove(yt.title+".mp4")

    #Gets colour change using dist formula
    def colourDist(self, col1, col2):
        return sqrt((int(col2[0]) - int(col1[0]))**2 + (int(col2[1]) - int(col1[1]))**2 + (int(col2[2]) - int(col1[2]))**2)

    #Takes black and white cv edge frame and finds stripe patterns
    def stripeVal(self, Eframe):
        print(Eframe[0])
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
        angleTots = [0, 0, 0, 0, 0, 0]
        for i in lineList:
            for j in i:
                angleTots[int(atan(j[1])//(pi/6))] += j[0]**5
        s = sqrt(sum([i**1.2 for i in angleTots]))/136 #maximum of 1, value of stripe count found
        #print(s)
        return s

    #Gets basic contrast of Cframe (0 to 100)
    def totContrast(self, Cframe):
        s = 0
        for i in Cframe:
            for col in i:
                s += col/(self.width*self.maxDist)
        s /= self.height
        s = s**0.4
        s *= 100
        return s

    #Sends fixed score to server
    def sendScore(self):
        start = max(0, len(self.scores)-10)
        print(sum(self.scores[start:len(self.scores)])/(len(self.scores)-start))
        #Send to database


    #Creates the contrast frame between two frames and gets epilepsy value
    def getContrast(self, frame1, frame2):
        contrastFrame = [[0 for i in range(self.width)]for j in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                contrastFrame[i][j] = self.colourDist(frame1[i][j], frame2[i][j])
        cv2.imwrite('cvimg.png', frame1) #Somehow convert pixelarray for frame1 into a png
        edges = cv2.Canny(frame1, 50, 300)
        return (self.totContrast(contrastFrame))# + self.stripeVal(edges))/2


test = video("https://www.youtube.com/watch?v=LHCob76kigA&list=RDLHCob76kigA&start_radio=1&t=59")