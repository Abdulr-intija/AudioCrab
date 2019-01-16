from scipy.io import wavfile
import numpy as np
import WavProcessor

class WavUnbox:

    def __init__(self, audioType):
        self.audioType = audioType

    def unbox(self, wavPath):
        # Read the wav file
        samplingFrequency, sampleAmplitudes = wavfile.read(wavPath)

        #strip out one channel(right) if more than one exist
        sampleData = np.array([sample[0] for sample in sampleAmplitudes])

        #if stereo, get second sample arrray
        rightSampleData = None
        if (self.audioType == "stereo"):
            rightSampleData = np.array([sample[1] for sample in sampleAmplitudes])
        
        WavProcessor.WavProcessor(wavPath).process(sampleData, rightSampleData, samplingFrequency)