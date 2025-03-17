import pandas as pd
import os

#tolabel the menu items with time
directory_path = 'D:\\uber eats\\night'


for filename in os.listdir(directory_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory_path, filename)
        
        data = pd.read_csv(file_path)
        
        data['Time of Day'] = 'night'
        
        data.to_csv(file_path, index=False)

        print(f'Updated file: {filename}')
