# from pytube import YouTube
from pprint import *
# counter=0
# yt = YouTube('https://www.youtube.com/watch?v=t_5IWiQutlw')
# qualityList=["360p","144p","240p","480p","720p"]
# bol=True
# while bol:
#     edited=yt.streams.filter(res=qualityList[counter],only_audio=False,mime_type="video/mp4").all()
#     if len(edited)==0:
#         counter+=1
#     else:
#         bol=False
# stream=yt.streams.filter(res=qualityList[counter],only_audio=False,mime_type="video/mp4").first()
# stream.download()

import cv2
cap = cv2.VideoCapture('C:/Users/nizar/PycharmProjects/Hack-the-North-Thing/extension/The Chainsmokers & Coldplay - Something Just Like This (Lyric).mp4')
frameList=[]
while(cap.isOpened()):
    ret, frame = cap.read()
    frameList.append(frame)
    if ret:
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
pprint(frameList)

