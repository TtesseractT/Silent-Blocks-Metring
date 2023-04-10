import subprocess
import re
import datetime

# Get the path to the video file from the command line argument
import sys
if len(sys.argv) < 2:
    print("Please provide the path to the video file as a command line argument.")
    sys.exit()
input_file = sys.argv[1]

# Run FFMPEG to extract the audio stream from the video file
subprocess.run(["ffmpeg", "-i", input_file, "-vn", "-acodec", "copy", "temp_audio.wav"], check=True)

# Use FFMPEG to analyze the audio and output the times of silence
output = subprocess.check_output(["ffmpeg", "-i", "temp_audio.wav", "-af", "silencedetect=n=-50dB:d=10", "-f", "null", "-"], stderr=subprocess.STDOUT)

# Parse the FFMPEG output to extract the start and end times of each silent period
silence_times = []
for line in output.decode().split("\n"):
    match = re.search(r"silence_start: (\d+\.\d+)", line)
    if match:
        start_time = float(match.group(1))
    match = re.search(r"silence_end: (\d+\.\d+)", line)
    if match:
        end_time = float(match.group(1))
        if end_time - start_time > 4.0:
            silence_times.append((start_time, end_time))

# Write the results to a text file
with open("silence_report.txt", "w") as f:
    for start, end in silence_times:
        start_time = str(datetime.timedelta(seconds=start))[:-3]
        end_time = str(datetime.timedelta(seconds=end))[:-3]
        duration = end - start
        f.write(f"[{start_time} --> {end_time}] = Silence Time: {duration:.2f}\n")
