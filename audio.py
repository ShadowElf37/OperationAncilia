import pyaudio
import wave
import threading
from time import sleep

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
AUDIO = pyaudio.PyAudio()

REFRESH = 0.0000001


class Throughput:
    def __init__(self):
        self.buffer = []
        self.open = False
        self.stream = None

    def pause(self):
        self.open = False
        self.stream.stop_stream()

    def unpause(self):
        self.open = True
        self.stream.start_stream()

    def close(self):
        self.stream.stop_stream()
        self.stream.close()


class AudioInput(Throughput):
    def __init__(self):
        super().__init__()
        self.stream = AUDIO.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
        self.buffer = []

    def activate(self):
        self.open = True
        while True:
            sleep(REFRESH)
            if self.open:
                self.buffer.append(self.stream.read(CHUNK))
                if len(self.buffer) > 500:
                    self.buffer.pop(0)

    def read(self):
        while not self.buffer:
            sleep(REFRESH)
            #return ''
        return self.buffer.pop(0)


class AudioOutput(Throughput):
    def __init__(self):
        super().__init__()
        self.stream = AUDIO.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, output=True,
                    frames_per_buffer=CHUNK)
        self.buffer = []

    def activate(self):
        self.open = True
        while True:
            sleep(REFRESH)
            if self.open:
                try:
                    self.stream.write(self.buffer.pop(0))

                except IndexError:
                    continue

    def write(self, data):
        self.buffer.append(data)


class AudioDevice:
    def __init__(self):
        self.inp = AudioInput()
        self.out = AudioOutput()
        self.ithread = None
        self.othread = None

    def read(self):
        if not self.inp.open:
            print('Stream closed.')
            return ''
        return self.inp.read()

    def write(self, data):
        if not self.out.open:
            print('Stream closed.')
            return ''
        self.out.write(data)

    def activate(self):
        self.ithread = threading.Thread(target=self.inp.activate, daemon=True)
        self.othread = threading.Thread(target=self.out.activate, daemon=True)
        self.ithread.start()
        self.othread.start()

    def mute(self):
        self.inp.pause()
    def unmute(self):
        self.inp.unpause()

    def deafen(self):
        self.out.pause()
    def undeafen(self):
        self.out.unpause()

    def close(self):
        self.out.close()
        self.inp.close()
        self.ithread = None
        self.othread = None


if __name__ == '__main__':
    d = AudioDevice()
    d.activate()
    while True:
        d.write(d.read())
