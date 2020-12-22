from os import confstr
import pathlib
import datetime
import moviepy.editor

mp4Path = 'mp4-file-path'
fname = pathlib.Path(mp4Path)

def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return hours, mins, seconds
def timestampToDate(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp))

utc8 = 8 * 60 * 60
with open('result.srt', 'w', encoding="utf-8") as outfile:
    if fname.exists():
        video = moviepy.editor.VideoFileClip(mp4Path)
        createTimestamp = fname.stat().st_birthtime
        videoDuration = int(video.duration)
        for i in range(0, videoDuration):
            thisRealTimestamp = fname.stat().st_birthtime + i
            thisVideoTimestamp = thisRealTimestamp - createTimestamp - utc8
            oneSecondLaterVideoTimestamp = thisVideoTimestamp + 1
            outfile.write(str(i + 1) + "\n")
            outfile.write(timestampToDate(thisVideoTimestamp).split()[1] + ",000" + " --> " + timestampToDate(oneSecondLaterVideoTimestamp).split()[1] + ",000" + "\n")
            outfile.write(timestampToDate(thisRealTimestamp) + "\n")
            outfile.write("\n")

