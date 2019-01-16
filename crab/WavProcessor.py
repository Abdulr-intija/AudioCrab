'''Terminologies-----
    PATTERN, refers to path through which the audio signal passes from your left speaker to the right
    GENERATOR BREAK, means the last break time while generating the pattern above in segments. 1 sample takes 'inverse of the audio sampling frequency' seconds to play, usually 1/44100 seconds
    LEFT DATA, means sample data on the left speaker
    RIGHT DATA, means sample data on the right speaker
'''

#int.
import os
import subprocess
import time
import random

#ext.
import numpy as np
from scipy.io import wavfile


class WavProcessor:

    def __init__(self, absoluteAudioPath):
        self.absoluteAudioPath = absoluteAudioPath

    def process(self, leftData, rightData, sampleFrequency):
        self.leftData = leftData
        self.rightData = rightData
        self.sampleFrequency = sampleFrequency

        t = time.time()
        waveLength = sampleFrequency * 16 #sum of wavelength per revolution of sound around baba's head
        self.waveLength = waveLength

        sinePad = self.generateSinePadding(waveLength, self.generatePattern())

        print("Still on the work...\n")
        self.reverb()

        print("Constraining samples and Finalizing...\n")
        finalSampleData = self.injectSinePad(sinePad)

        
        #--------- Portion below in this fucntion will be moved to WavRebox.py soon -----------
        #save
        print("Saving...\n")
        wavfile.write(self.absoluteAudioPath + '.wav', sampleFrequency, np.array(finalSampleData))

        print("Converting to mp3...")
        subprocess.call(['ffmpeg', '-i', self.absoluteAudioPath + '.wav', self.absoluteAudioPath + '.wav.mp3'])


        print("Time spent: ", time.time() - t, " secs")

        #remove tmp files
        if os.path.exists(self.absoluteAudioPath + '.wav'):
            os.remove(self.absoluteAudioPath + '.wav')
        
        if os.path.exists(self.absoluteAudioPath):
            os.remove(self.absoluteAudioPath)


    def generateSinePadding(self, waveLength, pattern):
        result = []
        generatorBreak = 0
        timeSpeedUpMoment = waveLength * 2

        for sineCount in pattern:
            steps = int(waveLength / sineCount)
            waveFrequency = 2
            speedup = sineCount > 2

            if speedup:
                spedWavelength = int(waveLength * 0.2)
            else:
                spedWavelength = waveLength

            for index in range(generatorBreak, generatorBreak + spedWavelength, steps):
                
                wave = self.sine(index, index + steps, waveFrequency)
                result += wave

            if speedup:
                steps = int(waveLength * 0.5)
                for index in range(generatorBreak + spedWavelength, generatorBreak + (spedWavelength * 5), steps):
                
                    wave = self.sine(index, index + steps, waveFrequency)
                    result += wave
        
            generatorBreak += (spedWavelength * 5)
        
        return result

    def sine(self, minAmplitude, maxAmplitude, freq):

        x = np.arange(minAmplitude, maxAmplitude)
        x_range = maxAmplitude - minAmplitude

        return [(np.sin(np.pi * freq * (amp/x_range)) * 10) for amp in x]

    def generatePattern(self):

        pattern = []
        patternRange = int(len(self.leftData) / self.waveLength) + 1

        for index in range(patternRange):
            #for now, random revoulution pattern
            sineCount = random.randint(1, 2)

            if index > 0 and index % 2 == 0:
                sineCount *= 5
                

            pattern.append(sineCount)
        
        return pattern

    def reverb(self):
        oldLeftData = self.leftData
        reverbLeakPool = [0 for i in range(2300)]

        self.leftData = np.concatenate([self.leftData, np.array(reverbLeakPool)])

        if self.rightData is None:
            self.rightData = self.leftData
        else:
            self.rightData = np.concatenate([self.rightData, np.array(reverbLeakPool)])

        # Reverb delay reduced in right speaker to form some sort of exponential reverb within the 2200/44100 secs time frame
        for index, sample in enumerate(oldLeftData):
            scaledDownSample = int(sample) * 0.5
            self.leftData[index + 1650] = (self.leftData[index + 1650] * 0.5) + scaledDownSample
            self.leftData[index + 2300] = (self.leftData[index + 2300] * 0.5) + scaledDownSample

            self.rightData[index + 975] = (self.rightData[index + 975] * 0.5) + scaledDownSample
            self.rightData[index + 1300] = (self.rightData[index + 1300] * 0.5) + scaledDownSample

    def injectSinePad(self, sinePad):

        resultData = []

        for i, sample in enumerate(self.leftData):
            left = int(sample)
            right = left

            if self.rightData is not None:
                right = int(self.rightData[i])

            tracePoint = sinePad[i]
       
            left *= (tracePoint + 20)
            right *= (tracePoint - 20)
        
            resultData.append([(np.int32)(left * 0.046), (np.int32)(right * 0.046)])

        return resultData