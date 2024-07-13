import os
import time
import threading
import tkinter as tk
from pvrecorder import PvRecorder
import wave, struct
from playsound import playsound
from allosaurus.app import read_recognizer
from allosaurus.model import get_all_models
from glob import glob
import random
from ToolTipClass import *
import webbrowser

class VoiceRecorder:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x500")
        self.root.title("Phoneunciation")

        # ai audio word
        self.model_fao = read_recognizer('fa2024')
        self.audio_files = glob('words/*.wav')
        self.audio_files_len = len(glob('words/*.wav'))
        self.randomn = random.randrange(0,self.audio_files_len)
        self.rand_audio = self.audio_files[self.randomn]
        self.wordtext = self.rand_audio.removeprefix('words/').removesuffix('.wav')

        self.modelphones = self.get_phones(self.rand_audio, 0)
        self.modelphones_colors = ["green"] * len(self.modelphones)
        self.modelphones_prob = self.get_phones(self.rand_audio, 1)
        self.modelphones_second = self.get_phones(self.rand_audio, 2)
        self.modelphones_second_colors = ["yellow"] * len(self.modelphones_second)
        self.modelphones_second_prob = self.get_phones(self.rand_audio, 3)
        self.modelphones_third = self.get_phones(self.rand_audio, 4)
        self.modelphones_third_colors = ["orange"] * len(self.modelphones_third)
        self.modelphones_third_prob = self.get_phones(self.rand_audio, 5)

        # frame
        self.labelframe = tk.Frame(self.root)
        self.labelframe.columnconfigure(0, weight=1)
        self.labelframe.columnconfigure(1, weight=1)

        self.label1 = tk.Label(self.labelframe, text="Reference", font=('Arial', 18))
        self.label1.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.label2 = tk.Label(self.labelframe, text="Feedback", font=('Arial', 18))
        self.label2.grid(row=0, column=1, sticky=tk.W+tk.E)

###
        self.label3 = tk.Label(self.labelframe, text="The colored phones are generated from the audio below", font=('Arial', 12))
        self.label3.grid(row=1, column=0, padx=10, pady=(0,20), sticky=tk.W+tk.E)

        self.label4 = tk.Label(self.labelframe, text="Record the word below and get feedback on the pronunciation", font=('Arial', 12))
        self.label4.grid(row=1, column=1, padx=10, pady=(0,20), sticky=tk.W+tk.E)

###
        self.labelframe2 = tk.Frame(self.labelframe)
        self.labelframe2.columnconfigure(0, weight=1)
        self.labelframe2.columnconfigure(1, weight=1)
        self.labelframe2.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W+tk.E)

        self.label5 = tk.Label(self.labelframe2, text="Word: " + self.wordtext + " ⧉", font=('Arial', 16)) # command=lambda: webbrowser.open_new("https://example.com")
        self.label5.grid(row=0, column=0, sticky=tk.W)
        CreateToolTip(self.label5, text="Click link.")
        self.label5.bind("<Button-1>", lambda e:webbrowser.open_new("https://sprotin.fo/dictionaries?_SearchInflections=0&_SearchDescriptions=0&_DictionaryId=2&_DictionaryPage=1&_SearchFor="+self.wordtext))

        self.button1 = tk.Button(self.labelframe2, text="🔊", font=('Arial', 18), command= self.play_AI)
        self.button1.grid(row=0, column=1, sticky=tk.W)
        CreateToolTip(self.button1, text="Listen to the reference word.")

        self.labelframe3 = tk.Frame(self.labelframe)
        self.labelframe3.columnconfigure(0, weight=1)
        self.labelframe3.columnconfigure(1, weight=1)
        self.labelframe3.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W+tk.E)

        self.label6 = tk.Label(self.labelframe3, text="Word: " + self.wordtext + " ⧉", font=('Arial', 16))
        self.label6.grid(row=0, column=0, sticky=tk.W)
        CreateToolTip(self.label6, text="Click link.")
        self.label6.bind("<Button-1>", lambda e:webbrowser.open_new("https://sprotin.fo/dictionaries?_SearchInflections=0&_SearchDescriptions=0&_DictionaryId=2&_DictionaryPage=1&_SearchFor="+self.wordtext))

        self.button2 = tk.Button(self.labelframe3, text="🔊", font=('Arial', 18), command= self.play_you)
        self.button2.grid(row=0, column=1, sticky=tk.W)
        CreateToolTip(self.button2, text="Listen to your recording.")


###
        self.labelframe4 = tk.Frame(self.labelframe)
        self.labelframe4.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.label7 = tk.Label(self.labelframe4, text="Closest phones: ⓘ ", font=('Arial', 16))
        self.label7.grid(row=0, column=0, sticky=tk.W)
        self.label7_labels = []
        for index,word in enumerate(self.modelphones):
            self.label7_1 = tk.Label(self.labelframe4, text=word, font=('Arial', round(10+(30*self.modelphones_prob[index]))), fg=self.modelphones_colors[index])
            self.label7_1.grid(row=0, column=index+1, sticky=tk.W)
            self.label7_labels.append(self.label7_1)
        CreateToolTip(self.label7, text="The closest probable phones are green.\nThe font size of each phone is generated based on probability.")

        self.labelframe5 = tk.Frame(self.labelframe)
        self.labelframe5.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        self.label8 = tk.Label(self.labelframe5, text="Closest phones: ⓘ ", font=('Arial', 16))
        self.label8.grid(row=0, column=0, sticky=tk.W)
        self.label8_labels = []
        CreateToolTip(self.label8, text="If a phone is red the phone is incorrect.")

###
        self.labelframe6 = tk.Frame(self.labelframe)
        self.labelframe6.grid(row=4, column=0, padx=10, pady=(10,0), sticky=tk.W)
        self.label9 = tk.Label(self.labelframe6, text="Second closest phones: ⓘ ", font=('Arial', 16))
        self.label9.grid(row=0, column=0, sticky=tk.W)
        self.label9_labels = []
        for index,word in enumerate(self.modelphones_second):
            self.label9_1 = tk.Label(self.labelframe6, text=word, font=('Arial', round(10+(30*self.modelphones_second_prob[index]))), fg=self.modelphones_second_colors[index])
            self.label9_1.grid(row=0, column=index+1, sticky=tk.W)
            self.label9_labels.append(self.label9_1)
        CreateToolTip(self.label9, text="The second closest probable phones are yellow.\nThe font size of each phone is generated based on probability.\n<blk> is blank and can be ignored.")

        self.label10 = tk.Label(self.labelframe, font=('Arial', 16))
        self.label10.grid(row=4, column=1, padx=10, pady=(10,0), sticky=tk.W)

###
        self.labelframe7 = tk.Frame(self.labelframe)
        self.labelframe7.grid(row=5, column=0, padx=10, pady=(0,10), sticky=tk.W)
        self.label11 = tk.Label(self.labelframe7, text="Thrid closest phones: ⓘ ", font=('Arial', 16))
        self.label11.grid(row=0, column=0, sticky=tk.W)
        self.label11_labels = []
        for index,word in enumerate(self.modelphones_third):
            self.label11_1 = tk.Label(self.labelframe7, text=word, font=('Arial', round(10+(30*self.modelphones_third_prob[index]))), fg=self.modelphones_third_colors[index])
            self.label11_1.grid(row=0, column=index+1, sticky=tk.W)
            self.label11_labels.append(self.label11_1)
        CreateToolTip(self.label11, text="The third closest probable phones are orange.\nThe font size of each phone is generated based on probability.\n<blk> is blank and can be ignored.")

        self.label12 = tk.Label(self.labelframe, text="", font=('Arial', 16))
        self.label12.grid(row=5, column=1, padx=10, pady=(0,10), sticky=tk.W+tk.E)

###
        self.buttonshuffle = tk.Button(self.labelframe, text="New word", font=('Arial', 18, "bold"), command= self.shuffle_word)
        self.buttonshuffle.grid(row=7, column=0, padx=10, pady=(40,0), sticky=tk.W+tk.E)

        self.buttonrecord = tk.Button(self.labelframe, text="◉", fg="red", font=('Arial', 18), command= self.click_handler)
        self.buttonrecord.grid(row=7, column=1, padx=10, pady=(40,0), sticky=tk.W+tk.E)
        
###
        self.labeltime = tk.Label(self.labelframe, text="00:00:00")
        self.labeltime.grid(row=8, column=1, padx=10, sticky=tk.W+tk.E+tk.N)

        self.labelframe.pack(fill='x')

        self.recording = False

        self.root.mainloop()
    
    def click_handler(self):
        if self.recording:
            self.recording = False
            self.buttonrecord.config(fg="red")
            self.buttonrecord.config(text="◉")
            
            self.label8.after(1000, self.update_you_phone)
        else:
            self.recording = True
            self.buttonrecord.config(fg="red")
            self.buttonrecord.config(text="❚❚")
            threading.Thread(target=self.record).start()

    def update_you_phone(self):
        newphones = self.get_phones('audio_recording.wav', 0)
        newphones_colors = ["red"] * len(newphones)
        newphones_prob = self.get_phones('audio_recording.wav', 1)

        # if I want the probability size from the reference, then uncomment in the for loop
        for index,p in enumerate(newphones):
            if len(self.modelphones) >= index+1:
                if p == self.modelphones[index]:
                    newphones_colors[index] = "green"
                    #newphones_prob[index] = self.modelphones_prob[index]
                if p == self.modelphones_second[index]:
                    newphones_colors[index] = "yellow"
                    #newphones_prob[index] = self.modelphones_second_prob[index]
                if p == self.modelphones_third[index]:
                    newphones_colors[index] = "orange"
                    #newphones_prob[index] = self.modelphones_third_prob[index]

        for l in self.label8_labels:
            l.destroy()
        self.label8_labels.clear()

        for index,word in enumerate(newphones):
            self.label8_1 = tk.Label(self.labelframe5, text=word, font=('Arial', round(10+(30*newphones_prob[index]))), fg=newphones_colors[index])
            self.label8_1.grid(row=0, column=index+1, sticky=tk.W)
            self.label8_labels.append(self.label8_1)

        if len(newphones_colors) == 0:
            self.label12.config(text="")
        elif "red" not in newphones_colors and "orange" not in newphones_colors and "yellow" not in newphones_colors:
            self.label12.config(text="Perfect! Try a new word.")
        elif "red" in newphones_colors:
            self.label12.config(text="Try again.")
        else:
            self.label12.config(text="Great.")

    def record(self):
        recorder = PvRecorder(device_index=0, frame_length= 512) #(32 milliseconds of 16kHz audio)
        audio = []
        path = 'audio_recording.wav'
        recorder.start()

        start = time.time()

        while self.recording:
            frame = recorder.read()
            audio.extend(frame)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.labeltime.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

        recorder.stop()
        with wave.open(path, 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h"* len(audio), *audio))
        recorder.delete()

    def play_AI(self):
        playsound(self.audio_files[self.randomn])

    def play_you(self):
        playsound('audio_recording.wav')

    def shuffle_word(self):
        self.randomn = random.randrange(0,self.audio_files_len)
        self.wordtext = self.audio_files[self.randomn].removeprefix('words/').removesuffix('.wav')
        self.label5.config(text="Word: " + self.wordtext + " ⧉")
        self.label6.config(text="Word: " + self.wordtext + " ⧉")

        self.modelphones = self.get_phones(self.audio_files[self.randomn], 0)
        self.modelphones_colors = ["green"] * len(self.modelphones)
        self.modelphones_prob = self.get_phones(self.audio_files[self.randomn], 1)

        self.modelphones_second = self.get_phones(self.audio_files[self.randomn], 2)
        self.modelphones_second_colors = ["yellow"] * len(self.modelphones_second)
        self.modelphones_second_prob = self.get_phones(self.audio_files[self.randomn], 3)

        self.modelphones_third = self.get_phones(self.audio_files[self.randomn], 4)
        self.modelphones_third_colors = ["orange"] * len(self.modelphones_third)
        self.modelphones_third_prob = self.get_phones(self.audio_files[self.randomn], 5)

        for l in self.label7_labels:
            l.destroy()
        self.label7_labels.clear()
        for l in self.label8_labels:
            l.destroy()
        self.label8_labels.clear()
        for l in self.label9_labels:
            l.destroy()
        self.label9_labels.clear()
        for l in self.label11_labels:
            l.destroy()
        self.label11_labels.clear()

        for index,word in enumerate(self.modelphones):
            self.label7_1 = tk.Label(self.labelframe4, text=word, font=('Arial', round(10+(30*self.modelphones_prob[index]))), fg=self.modelphones_colors[index])
            self.label7_1.grid(row=0, column=index+1, sticky=tk.W)
            self.label7_labels.append(self.label7_1)
        self.label8_1 = tk.Label(self.labelframe5, font=('Arial', 16))
        self.label8_1.grid(row=0, column=index+1, sticky=tk.W)
        self.label8_labels.append(self.label8_1)
        for index,word in enumerate(self.modelphones_second):
            self.label9_1 = tk.Label(self.labelframe6, text=word, font=('Arial', round(10+(30*self.modelphones_second_prob[index]))), fg=self.modelphones_second_colors[index])
            self.label9_1.grid(row=0, column=index+1, sticky=tk.W)
            self.label9_labels.append(self.label9_1)
        self.label12.config(text="")
        for index,word in enumerate(self.modelphones_third):
            self.label11_1 = tk.Label(self.labelframe7, text=word, font=('Arial', round(10+(30*self.modelphones_third_prob[index]))), fg=self.modelphones_third_colors[index])
            self.label11_1.grid(row=0, column=index+1, sticky=tk.W)
            self.label11_labels.append(self.label11_1)

    # first_priority i=0, second_priority i=2, third_priority i=4, first_probability i=1, second_probability i=3, third_probability i=5
    def get_phones(self, audio, i):
        phones = self.model_fao.recognize(audio, 'fao', topk=3)
        if phones == "":
            return ""
        phones = phones.split("|")
        output_phones= ""
        
        for p in phones:
            if (p[0] == " "):
                p = p[1:]
            if (p[len(p)-1] == " "):
                p = p[:-1]
                
            p = p.split(" ")
            output_phones += p[i] + " "
            
        output_phones = output_phones.split(" ")
        output_phones = output_phones[:-1]

        if i == 1 or i == 3 or i == 5:
            for index,o in enumerate(output_phones):
                o = o.replace("(","")
                o = o.replace(")","")
                output_phones[index] = eval(o)
        
        return output_phones
            
VoiceRecorder()
