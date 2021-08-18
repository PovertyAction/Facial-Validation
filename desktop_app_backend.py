
# coding: utf-8

# # Instructions
#
# 1. This script is meant to assist in the validation of identity using facial recognition.
#
# 2. If running it in Jupyter Notebook, press 'shift + return' or 'shift + enter' to navigate through the script and fill in the prompts when asked.
#
# 3. If you have any errors or feedback, contact jjacobson@poverty-action.org or researchsupport@poverty-action.org
#
# (If this script is loaded via Jupyter Notebook, despite loading in the browser, it is running locally on your machine and will continue to run fine regardless of internet access.)

# # Import and Set-up

# In[1]:

import sys
import os
import glob

import pandas as pd
import time
import warnings
import facial_validation_processor as fvp
warnings.filterwarnings("ignore")

def smart_print(the_message, messages_pipe = None):
    if __name__ == "__main__":
        print(the_message)
    else:
        messages_pipe.send(the_message)

def smart_return(to_return, function_pipe = None):
    if __name__ != "__main__":
        function_pipe.send(to_return)
    else:
        if len(to_return) == 2:
            return to_return[0], to_return[1]
        else:
            return to_return


def read_files_and_analyze_images(arguments_pipe, messages_pipe):
    #file_pairings = pd.read_excel('Filenames.xlsx')
    dataset_path = arguments_pipe.recv()
    dataset_path_l = dataset_path.lower()

    raise_error = False
    status_message = False

    try:
        if dataset_path_l.endswith(('xlsx', 'xls')):
            dataset = pd.read_excel(dataset_path)
        elif dataset_path_l.endswith('csv'):
            dataset = pd.read_csv(dataset_path)
        elif dataset_path_l.endswith('dta'):
            try:
                dataset = pd.read_stata(dataset_path)
            except ValueError:
                dataset = pd.read_stata(dataset_path, convert_categoricals=False)
        elif dataset_path_l.endswith('vc'):
            status_message = "**ERROR**: This folder appears to be encrypted using VeraCrypt."
            raise Exception
        elif dataset_path_l.endswith('bc'):
            status_message = "**ERROR**: This file appears to be encrypted using Boxcryptor. Sign in to Boxcryptor and then select the file in your X: drive."
            raise Exception
        else:
            raise Exception

    except (FileNotFoundError, Exception):
        if status_message is False:
            status_message = '**ERROR**: This path appears to be invalid. If your folders or filename contain colons or commas, try renaming them or moving the file to a different location.'
        smart_print(status_message, messages_pipe)
        raise

    # Parse pandas dataframe for these
    images_directory_path = dataset.iloc[0,1]
    file_pairings = dataset.iloc[3:,:2]
    file_pairings.columns = dataset.iloc[2,:2]
    file_pairings = file_pairings.reset_index(drop=True)

    if images_directory_path.endswith(('"', "'")):
        images_directory_path = images_directory_path[1:-1]

    if not images_directory_path.endswith(('/', "\\")):
        if '/' in images_directory_path:
            images_directory_path = images_directory_path + '/'
        elif '\\' in images_directory_path:
            images_directory_path = images_directory_path + '\\'


    #Update relative to absolute routes in file_pairings
    for row_index in range(file_pairings.shape[0]):
        for col_index in range(2):
            #Add directory path
            file_pairings.iloc[row_index, col_index] = images_directory_path + str(file_pairings.iloc[row_index, col_index])

    status_message = '**SUCCESS**: The template has been read successfully.'
    smart_print(status_message, messages_pipe)

    status_message = 'Analyzing images...'
    smart_print(status_message, messages_pipe)

    status_message, file_pairings = fvp.process_images(file_pairings)
    smart_print(status_message, messages_pipe)

    status_message, file_pairings = fvp.compare_images(file_pairings)

    #Save result
    file_pairings.to_csv(images_directory_path + 'results.csv', index=False)

    smart_print(status_message, messages_pipe)
