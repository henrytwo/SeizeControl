from math import *
import urllib.request

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
        name = "tmpvid.mp4"
        urllib.request.urlretrieve(self.url, name)

        self.vid = 0
        self.width = 0
        self.height = 0

    #Takes video and makes frame array
    def getFrames(self):
        self.frameArray = []
        self.frameCount = len(self.frameArray)

    #Creates the contrast frame between two frames
    def getContrast(self, frame1, frame2):
        contrastFrame = [[0 for i in range(self.width)]for j in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                contrastFrame[i][j] = sqrt((frame2[i][j][0] - frame1[i][j][0])**2 + (frame2[i][j][1] - frame1[i][j][1])**2 + (frame2[i][j][2] - frame1[i][j][2])**2)
        return self.getContrastScore(contrastFrame)

    #Takes contrast frame and gets epilepsy score
    def getContrastScore(self, Cframe):
        total = 0
        total += self.totContrast(Cframe)
        return total

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
            score = self.getContrastScore(self.getContrast(self.frameArray[i], self.frameArray[i+1]))
            self.scores.append(score)
            self.sendScore(i)

    #Code to delete the video file downloaded
    def die(self):
        pass

test = video("https://www.youtube.com/watch?v=fhiHqz8Ur24")