import numpy
import math
import sounddevice


class SineTone:
	#we create  class to access 

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



def measure_audiogram(frequency: float) -> tuple[float, float]:
	print("test", frequency, "Hz")

	upper_threshold = math.nan
	lower_threshold = math.nan
	try:
		# 1.
		sine_tone = SineTone(frequency)

		# 2.
		#amplitude = 0
		amplitude = 1e-2
		while amplitude < 1:
			sine_tone.amplitude = amplitude 
			sine_tone.play_tone()
			response = input("Did you hear the sound? ('y' or 'n')")
			response = response.strip().lower()
			if response == "y":
				upper_threshold = amplitude
				print(f"the upper_threshold is {amplitude}")
				break
			elif response == "n":
				amplitude*=1.5
			else:
				return(math.nan, math.nan)

		amplitude*=0.8
		while amplitude > 0:
			sine_tone.amplitude = amplitude

			sine_tone.play_tone()
			response = input("Did you hear the sound? ('y' or 'n')")
			response = response.strip().lower()
			if response == "n":
				lower_threshold = amplitude
				print(f"the lower_threshold is {amplitude}")
				break
			elif response == "y":
				amplitude*=0.8
			else:
				return(math.nan, math.nan)

		return (lower_threshold, upper_threshold)

	finally:
		print('Reached upper threshold', upper_threshold)
		print('Reached lower threshold', lower_threshold)


def all_frequences(frequencies):
	measurement_matrix = numpy.zeros((2, len(frequencies)))
	i = 0
	for frequency in frequencies:
		lower_threshold, upper_threshold = measure_audiogram(frequency)
		measurement_matrix[i] = [lower_threshold, upper_threshold]
		i+=1
	print(measurement_matrix)
	return measurement_matrix

frequencies_all = [125, 250, 500, 1000, 2000, 4000, 8000, 16000]
frequencies = [125, 250]

measurement_matrix = all_frequences(frequencies)
print(measurement_matrix)

A_ref = 1.0
amplitudes_in_db = [20*numpy.log10(A / A_ref) for A in measurement_matrix]
#measurement_matrix = numpy.array([])

from matplotlib import pyplot
from matplotlib.axes import Axes

diagram: Axes = pyplot.axes()

diagram.plot(frequencies, amplitudes_in_db)

diagram.set(title="audiogram", ylabel="audible amplitude range [dB]", xlabel="frequency [Hz]")
diagram.set(xticks=numpy.arange(len(measurement_matrix)), xticklabels=frequencies)

pyplot.show()