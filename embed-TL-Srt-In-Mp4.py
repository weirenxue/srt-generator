import pathlib
import datetime
import moviepy.editor
import platform
import cv2 
import time
import sys
import os

def timestampToDate(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp))

inMp4Path = sys.argv[1] if len(sys.argv) >= 2 else ''
outMp4Path = sys.argv[2] if len(sys.argv) >= 3 else ''
createTime = sys.argv[3] if len(sys.argv) >= 4 else '' # yyyy/mm/dd HH:MM


if inMp4Path == '':
    print("Missing input mp4 file name.")
    exit(1)
if outMp4Path == '':
    print("Missing output mp4 file name.")
    exit(1)
    

if os.path.isfile(inMp4Path):
    fname = pathlib.Path(inMp4Path)
    video = moviepy.editor.VideoFileClip(inMp4Path)
    try:
        createTimestamp = time.mktime(datetime.datetime.strptime(createTime, "%Y/%m/%d %H:%M").timetuple())
    except ValueError:
        print('No assigned create time, using ctime get from filesystem.')
        createTimestamp = int(fname.stat().st_ctime)
        if platform.system() != 'Windows':
            createTimestamp = int(fname.stat().st_birthtime)
    print('Using \'' + timestampToDate(createTimestamp) + '\' as start time.')
    videoDuration = int(video.duration)
    fps = video.fps
    videoWidth = video.subclip(0, 10).w
    videoHeight = video.subclip(0, 10).h
    frames = video.fps * videoDuration
        

    cap = cv2.VideoCapture(inMp4Path) 
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    output_movie = cv2.VideoWriter(filename = outMp4Path, 
                                fourcc = fourcc, 
                                frameSize = (videoWidth, videoHeight), fps = fps)
    thisRealTimestamp = createTimestamp
    prevProgress = 0
    for i in range(1, int(frames) + 1): 
        curProgress = round((i/frames)*100)
        if curProgress != prevProgress:
            print(str(curProgress) + "%")
            prevProgress = curProgress
        dateTime = timestampToDate(thisRealTimestamp)
        if i % round(fps) == 0:
            thisRealTimestamp = thisRealTimestamp + 1
        ret, frame = cap.read() 
        font = cv2.FONT_HERSHEY_SIMPLEX 
        if frame is not None:
            cv2.rectangle(frame, (50, 25), (420, 60), (0, 0, 0), -1)
            cv2.putText(frame,  
                        dateTime,  
                        (50, 50),  
                        font, 1,  
                        (255, 255, 255),  
                        2,  
                        cv2.LINE_4) 
            output_movie.write(frame)
    cap.release() 
    cv2.destroyAllWindows() 
else:
    print(inMp4Path + " doesn't exist.")
