import sys
import matplotlib.pyplot as plt

labels = ['Cantonese', 'Hebrew', 'ClassicalCN', 'Thai', 'Polish', 'Spanish', 'Afrikaans', 'Sanskrit', 'Urdu', 'Japanese']
x = [0.00, 0.03, 0.05, 0.09, 0.25, 0.27, 0.81, 0.89, 0.95, 1.00]  # proportion of OV
y = [1.00, 0.97, 0.95, 0.91, 0.75, 0.73, 0.19, 0.11, 0.05, 0.00]  # proportion of VO
plt.plot(x, y, 'ro')
plt.title('Relative word order of verb and object')
plt.xlim([0,1]) # Set the x and y axis ranges
plt.ylim([0,1])
plt.xlabel('OV') # Set the x and y axis labels
plt.ylabel('VO')
for i, label in enumerate(labels):  # Add labels to each of the points
    plt.text(x[i]+0.02, y[i], label, fontsize=9)
    plt.savefig(sys.argv[1])
    plt.show()
