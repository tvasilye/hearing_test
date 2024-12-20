import numpy
import math
import sounddevice
import csv
import os
import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SineTone:
    def __init__(self, frequency=1000, amplitude=0.5, duration_seconds=1.5, sample_rate=48000):
        self.frequency = frequency
        self.amplitude = amplitude
        self.duration = duration_seconds
        self.sample_rate = sample_rate

        self.times = numpy.linspace(0, duration_seconds, int(duration_seconds * sample_rate)+1)

        circular_frequency = 2 * math.pi * frequency
        self.samples = numpy.sin(circular_frequency * self.times)
    
    def play_tone(self):
        sounddevice.play(self.amplitude * self.samples, self.sample_rate, blocking=True)

def write_to_csv(filename, data):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

def get_next_user_id(filename='hearing_test_results.csv'):
    if not os.path.exists(filename):
        return 1
    
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        
        try:
            ids = [int(row[0]) for row in reader if row]
            return max(ids) + 1 if ids else 1
        except (IndexError, ValueError):
            return 1

class HearingTestApp:
    def __init__(self, master):
        self.master = master
        self.file_path = file_path

        master.title("Hearing Test")
        master.geometry("500x500")

        self.label = tk.Label(master, text="Hearing Test", font=("Arial", 18))
        self.label.pack(pady=20)

        self.label2 = tk.Label(master, text="Could you hear the sound?",font=("Arial", 18))

        self.start_button = tk.Button(master, text="Start Test", command=self.start_test, font=("Arial", 14))
        self.start_button.pack(pady=10)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=20)


        self.disclaimer = tk.Label(
        master,
        text="The results of this hearing test are influenced by external factors such as the quality and calibration "
                "of your audio playback equipment (e.g., speakers or headphones) and environmental noise. This test is "
                "For accurate hearing diagnostics, please consult a licensed audiologist.",
        font=("Arial", 10),
        fg="darkred",
        wraplength=400,
        justify="center"
        )
        self.disclaimer.pack(side=tk.BOTTOM, pady=10)


        self.yes_button = tk.Button(self.button_frame, text="Yes", command=lambda: self.record_response("y"), 
                                    state=tk.DISABLED, bg="green", fg="white", font=("Arial", 14))
        self.yes_button.pack(side=tk.LEFT, padx=10)

        self.repeat_button = tk.Button(self.button_frame, text="Repeat", command=self.repeat_tone, 
                                       state=tk.DISABLED, font=("Arial", 14))
        self.repeat_button.pack(side=tk.LEFT, padx=10)

        self.no_button = tk.Button(self.button_frame, text="No", command=lambda: self.record_response("n"), 
                                   state=tk.DISABLED, bg="red", fg="white", font=("Arial", 14))
        self.no_button.pack(side=tk.LEFT, padx=10)

        self.frequencies = [125, 250, 500, 1000, 2000, 4000, 8000]
        self.current_frequency_index = 0
        self.current_amplitude = 1e-4
        self.measurement_matrix = numpy.zeros((len(self.frequencies), 2))
        
        self.userID = get_next_user_id()
        self.age = tk.IntVar()
        
        self.age_label = tk.Label(master, text="Enter Age:", font=("Arial", 14))
        self.age_label.pack(pady=5)
        self.age_entry = tk.Entry(master, textvariable=self.age, font=("Arial", 14))
        self.age_entry.pack(pady=5)

        self.finding_upper_threshold = True
        self.upper_threshold = None
        self.lower_threshold = None
        self.current_tone = None

    def start_test(self):
        if not self.age.get():
            messagebox.showerror("Error", "Please enter your age.")
            return
        
        self.age_label.pack_forget()
        self.age_entry.pack_forget()
        self.start_button.pack_forget()
        self.label2.pack(pady=10, before=self.button_frame)

        self.start_button.config(state=tk.DISABLED)
        self.yes_button.config(state=tk.NORMAL)
        self.no_button.config(state=tk.NORMAL)
        self.repeat_button.config(state=tk.NORMAL)
        self.age_entry.config(state=tk.DISABLED)
        self.test_next_frequency()

    def test_next_frequency(self):
        if self.current_frequency_index < len(self.frequencies):
            frequency = self.frequencies[self.current_frequency_index]

            self.label.config(text=f"Testing {frequency} Hz")
            print(f"Starting test for {frequency} Hz")
            #self.master.update_idletasks() 
            self.finding_upper_threshold = True
            self.upper_threshold = None
            self.lower_threshold = None
            self.current_amplitude = 1e-4
            self.play_tone(frequency)
        else:
            self.finish_test()

    def play_tone(self, frequency):
        self.current_tone = SineTone(frequency, amplitude=self.current_amplitude)
        self.current_tone.play_tone()

    def repeat_tone(self):
        if self.current_tone:
            self.current_tone.play_tone()

    def record_response(self, response):

        frequency = self.frequencies[self.current_frequency_index]

        if self.finding_upper_threshold:
            self._find_upper_threshold(frequency, response)
        else:
            self._find_lower_threshold(frequency, response)

        if self.current_frequency_index < len(self.frequencies):
            self.play_tone(self.frequencies[self.current_frequency_index])
        else:
            self.finish_test()

    def _find_upper_threshold(self, frequency, response):

        if response == "y":
            self.upper_threshold = self.current_amplitude
            print(f"Upper threshold set at {self.upper_threshold} for {frequency} Hz")
            self.finding_upper_threshold = False 
            self.current_amplitude *= 0.8 
        else:
            self.current_amplitude *= 1.5
            print(f"Increasing amplitude to {self.current_amplitude} for {frequency} Hz")
            if self.current_amplitude >= 1:
                self.finding_upper_threshold = False
                self.current_amplitude = self.upper_threshold if self.upper_threshold else 1e-2
                print(f"Upper threshold fallback to {self.current_amplitude} for {frequency} Hz")

    def _find_lower_threshold(self, frequency, response):

        if response == "n":
            self.lower_threshold = self.current_amplitude
            print(f"Lower threshold set at {self.lower_threshold} for {frequency} Hz")

            self.measurement_matrix[self.current_frequency_index] = [self.lower_threshold, self.upper_threshold]
            
            write_to_csv(
                self.file_path,
                [self.userID, self.age.get(), frequency, self.lower_threshold, self.upper_threshold],
            )

            self.current_frequency_index += 1
            self.test_next_frequency()
            self.finding_upper_threshold = True 
            self.current_amplitude = 1e-4
        else:
            self.current_amplitude *= 0.8
            print(f"Decreasing amplitude to {self.current_amplitude} for {frequency} Hz")

    def finish_test(self):
        self.yes_button.config(state=tk.DISABLED)
        self.no_button.config(state=tk.DISABLED)
        self.repeat_button.config(state=tk.DISABLED)
        messagebox.showinfo("Test Complete", "Hearing test finished!")
        self.show_audiogram()

    def show_audiogram(self):
        A_ref = 1.0
        lower_amplitudes_in_db = [20*numpy.log10(A[0] / A_ref) if A[0] > 0 else None for A in self.measurement_matrix]
        upper_amplitudes_in_db = [20*numpy.log10(A[1] / A_ref) if A[1] > 0 else None for A in self.measurement_matrix]

        fig, ax = pyplot.subplots()
        ax.plot(self.frequencies, lower_amplitudes_in_db, 'b-', label='Lower Threshold')
        ax.plot(self.frequencies, upper_amplitudes_in_db, 'r-', label='Upper Threshold')
        ax.set(title="Audiogram", ylabel="Audible amplitude range [dB]", xlabel="Frequency [Hz]")
        ax.set_xscale('log')
        ax.set_xticks(self.frequencies)
        ax.set_xticklabels(self.frequencies)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, 'hearing_test_results.csv')

    if not os.path.exists(file_path):
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['userID', 'age', 'frequency', 'lowerThreshold', 'upperThreshold'])

    root = tk.Tk()
    app = HearingTestApp(root)
    root.mainloop()
