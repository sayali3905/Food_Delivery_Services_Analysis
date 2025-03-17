import pandas as pd
import os

#to label morning, afternoon and night for each data
directory_path = 'D:\\grubhub\\morning'

for filename in os.listdir(directory_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory_path, filename)
        
        data = pd.read_csv(file_path)
        
        data['Time of Day'] = 'morning'
        
        data.to_csv(file_path, index=False)

        print(f'Updated file: {filename}')