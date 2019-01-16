import Entrance

#path to audio
print("Provide the full path to your audio file")
path = str(input())

#type of audio, defaults to mono if not supplied
print("\nWhat type of audio is this? Mono or Stereo")
audioType = str(input()).lower()

if audioType != "stereo" and audioType != "mono":
    audioType = "mono"

#Clean input. For now, just cut out quotes if present
path = path.replace("\"", "")

Entrance.Entrance(path).kickStart(audioType)