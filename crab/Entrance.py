import subprocess
import WavUnbox

class Entrance:

    def __init__(self, targetAudio):
        self.targetAudio = targetAudio

    def kickStart(self, audioType):

        splittedPath = self.targetAudio.split("\\") 
        fileName = splittedPath[len(splittedPath) -1]

        #convert to wav
        print("Converting to WAV...\n")
        subprocess.call(['ffmpeg', '-i', self.targetAudio, '-acodec', 'pcm_s32le', self.targetAudio + '.wav'])

        #unbox
        WavUnbox.WavUnbox(audioType).unbox(self.targetAudio + '.wav')


