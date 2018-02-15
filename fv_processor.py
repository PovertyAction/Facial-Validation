
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
import dlib
import glob
from skimage import io
from sklearn.metrics.pairwise import euclidean_distances
import pandas as pd
from tqdm import tqdm #Optional, for tracking progress of for loop
import time
import warnings
warnings.filterwarnings("ignore")

# Set-up of parameters
## Facial detection
detector = dlib.get_frontal_face_detector()

## Landmark extraction
if hasattr(sys, "_MEIPASS"):
    predictor_path = os.path.join(sys._MEIPASS, 'shape_predictor_68_face_landmarks.dat')
else:
    predictor_path = 'shape_predictor_68_face_landmarks.dat'

sp = dlib.shape_predictor(predictor_path)

## Facial recognition
if hasattr(sys, "_MEIPASS"):
    face_rec_model_path = os.path.join(sys._MEIPASS, 'dlib_face_recognition_resnet_model_v1.dat')
else:
    face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'

facerec = dlib.face_recognition_model_v1(face_rec_model_path)

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

def read_files(arguments_pipe, messages_pipe):
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

    status_message = '**SUCCESS**: The template has been read successfully.'
    smart_print(status_message, messages_pipe)

    status_message = 'Analyzing images...'
    smart_print(status_message, messages_pipe)

    # Precision parameter (lower number = faster runtime, less accuracy; speed of 1 -> 99.13% accuracy, 100 -> 99.38%)
    speed = 1

    ## Track and store information on each image as it is processed, as well as score; set Match Score default as missing
    file_pairings['Img1 Processed?'] = ''
    file_pairings['Img2 Processed?'] = ''
    file_pairings['Img1 Vector'] = ''
    file_pairings['Img2 Vector'] = ''
    file_pairings['Match Score'] = float(-222)

    for row_index in tqdm(range(file_pairings.shape[0])):
        for col_index in range(2):
            
            # Check for missing image; skip if missing
            image_name = file_pairings.iloc[row_index, col_index]
            if image_name != image_name:
                if col_index == 0:
                    file_pairings['Img1 Processed?'][row_index] = 0
                elif col_index == 1:
                    file_pairings['Img2 Processed?'][row_index] = 0
                continue
            
            # Read image and detect faces
            image_path = images_directory_path + image_name
            try:
                read_in_image = io.imread(image_path)

            except IOError:
                if col_index == 0:
                    #file_pairings['Img1 Processed?'][row_index] = 0
                    file_pairings['Img1 Processed?'][row_index] = 'File not found.'
                elif col_index == 1:
                    #file_pairings['Img2 Processed?'][row_index] = 0
                    file_pairings['Img2 Processed?'][row_index] = 'File not found.'
                continue
            
            faces = detector(read_in_image, 1)
            
            # If there is not exactly 1 face, skip
            if len(faces) != 1:
                if col_index == 0:
                    #file_pairings['Img1 Processed?'][row_index] = 0
                    file_pairings['Img1 Processed?'][row_index] = str(len(faces)) + ' faces found.'
                elif col_index == 1:
                    #file_pairings['Img2 Processed?'][row_index] = 0
                    file_pairings['Img2 Processed?'][row_index] = str(len(faces)) + ' faces found.'
                continue
      
            # Process the face and make vector
            shape = sp(read_in_image, faces[0])
            
            face_descriptor = facerec.compute_face_descriptor(read_in_image, shape, speed)        
            
            # Log successful processing and 128D vector
            if col_index == 0:
                file_pairings['Img1 Processed?'][row_index] = 1
                file_pairings['Img1 Vector'][row_index] = face_descriptor
            elif col_index == 1:
                file_pairings['Img2 Processed?'][row_index] = 1
                file_pairings['Img2 Vector'][row_index] = face_descriptor

            # If pair of images successfully processed, compute Euclidean distance
            if file_pairings['Img1 Processed?'][row_index] == 1 and file_pairings['Img2 Processed?'][row_index] == 1:
                file_pairings['Match Score'][row_index] = euclidean_distances(file_pairings['Img1 Vector'][row_index], file_pairings['Img2 Vector'][row_index])[0][0]

    status_message = 'Images processed, results being calculated...'
    smart_print(status_message, messages_pipe)

    threshold = 0.6 # Recommended accuracy from developers of model.
    percentage = 0
    # Flagging calculated scores that exceed Euclidean distance threshold
    if threshold != 0: # pass threshold = 0 to skip test
        file_pairings['Same Person: Threshold Test'] = ''
        
        for row_index in range(len(file_pairings)):
            # Check for valid Match Score and Score less than set threshold
            if file_pairings['Match Score'][row_index] != -222 and file_pairings['Match Score'][row_index] < threshold:
                file_pairings['Same Person: Threshold Test'][row_index] = 1.0
            elif file_pairings['Match Score'][row_index] != -222 and file_pairings['Match Score'][row_index] > threshold:
                file_pairings['Same Person: Threshold Test'][row_index] = 0.0
            elif file_pairings['Match Score'][row_index] == -222:
                file_pairings['Same Person: Threshold Test'][row_index] = -222
    
    # Flagging a set percentage of calculated scores, by greatest distance
    if percentage != 0: # pass percentage = 0 to skip test
        file_pairings['Same Person: Percentage Test'] = -222
        
        # Consider only valid values
        num_valid_values = len(file_pairings[file_pairings['Match Score']!=-222])
        minimum_valid_score = min(file_pairings[file_pairings['Match Score']!=-222]['Match Score'])
        
        # Sort by match score, figure out valid index range
        file_pairings = file_pairings.sort_values('Match Score')
        file_pairings.index = range(len(file_pairings))
        lowest_valid_value_index = list(file_pairings['Match Score']).index(minimum_valid_score)
        
        # Identify index cut-off based on specified percentage
        percent_index_highest_valid = int(num_valid_values * (1-percentage)) + lowest_valid_value_index #int rounds down, but the 0 index also means that 1 extra is being counted anyway
        
        # Assign
        file_pairings['Same Person: Percentage Test'][:lowest_valid_value_index] = -222
        file_pairings['Same Person: Percentage Test'][lowest_valid_value_index:percent_index_highest_valid] = 1
        file_pairings['Same Person: Percentage Test'][percent_index_highest_valid:] = 0
    
    file_pairings.to_csv(images_directory_path + 'results.csv', index=False)

    status_message = "Application finished. Results of analysis have been output to: " + images_directory_path + 'results.csv'
    smart_print(status_message, messages_pipe)