# import packages
import pandas as pd
import matplotlib.pyplot as plt


# Read in brca1/2 data; update path to final data sets from cleaning.py
brca1 = pd.read_csv('..path/final_brca1_data.csv')
brca2 = pd.read_csv('..path/final_brca2_data.csv')

# Create plot of expression levels
brca1['Expression'].plot()
plt.title('Plot of Expression in BRCA1')
plt.xlabel('BRCA1')
plt.grid(True)
plt.show()

brca2['Expression'].plot()
plt.title('Plot of Expression in BRCA2')
plt.xlabel('BRCA2')
plt.grid(True)
plt.show()

# Create plot for expressin and PSA
plt.scatter(brca1['PREOPERATIVE_PSA'], brca1['Expression'])
plt.title('Scatter Plot of PSA vs. Expression in BRCA1')
plt.xlabel('PSA')
plt.ylabel('Expression')
plt.grid(True)
plt.show()

plt.scatter(brca2['PREOPERATIVE_PSA'], brca2['Expression'])
plt.title('Scatter Plot of PSA vs. Expression in BRCA2')
plt.xlabel('PSA')
plt.ylabel('Expression')
plt.grid(True)
plt.show()
