import pathlib
import datetime
import moviepy.editor
import platform
import os

mp4Path = 'mp4-file-path'
fname = pathlib.Path(mp4Path)
filenmae = os.path.splitext(os.path.basename(fname))[0]

def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return hours, mins, seconds
def timestampToDate(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp))
def timestampToUtcDate(timestamp):
    return str(datetime.datetime.utcfromtimestamp(timestamp))

with open(filenmae + '.srt', 'w', encoding="utf-8") as outfile:
    if fname.exists():
        video = moviepy.editor.VideoFileClip(mp4Path)
        createTimestamp = int(fname.stat().st_ctime)
        if platform.system() != 'Windows':
            createTimestamp = int(fname.stat().st_birthtime)
        videoDuration = int(video.duration)
        for i in range(0, videoDuration):
            thisRealTimestamp = createTimestamp + i
            thisVideoTimestamp = thisRealTimestamp - createTimestamp
            oneSecondLaterVideoTimestamp = thisVideoTimestamp + 1
            outfile.write(str(i + 1) + "\n")
            outfile.write(timestampToUtcDate(thisVideoTimestamp).split()[1] + ",000" + " --> " + timestampToUtcDate(oneSecondLaterVideoTimestamp).split()[1] + ",000" + "\n")
            outfile.write(timestampToDate(thisRealTimestamp) + "\n")
            outfile.write("\n")
