import matplotlib.pyplot as plt

def visualize_results(frequencies, responses):
    fig, ax = plt.subplots()
    ax.plot(frequencies, responses, 'b-o')
    ax.set_xscale('log')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Response')
    ax.set_title('Hearing Test Results')
    ax.grid(True)
    plt.show()

# Beispielaufruf:
frequencies = [125, 250, 500, 1000, 2000, 4000, 8000]
responses = [1, 1, 1, 0, 1, 0, 0]
visualize_results(frequencies, responses)
