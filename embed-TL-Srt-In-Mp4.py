import pathlib
import datetime
import moviepy.editor
import platform
import cv2 
import time

inMp4Path = 'inMp4Path'
outMp4Path = 'outMp4Path'
createTime = 'yyyy/mm/dd HH:MM' # yyyy/mm/dd HH:MM

fname = pathlib.Path(inMp4Path)

def timestampToDate(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp))
if fname.exists():
    video = moviepy.editor.VideoFileClip(inMp4Path)
    try:
        createTimestamp = time.mktime(datetime.datetime.strptime(createTime, "%Y/%m/%d %H:%M").timetuple())
    except ValueError:
        print('No assigned create time, using ctime get from filesystem.')
        createTimestamp = int(fname.stat().st_ctime)
        if platform.system() != 'Windows':
            createTimestamp = int(fname.stat().st_birthtime)
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
            cv2.putText(frame,  
                        dateTime,  
                        (50, 50),  
                        font, 1,  
                        (0, 0, 0),  
                        2,  
                        cv2.LINE_4) 
            output_movie.write(frame)
    cap.release() 
    cv2.destroyAllWindows() 
