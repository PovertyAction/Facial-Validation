from os import listdir
from os.path import isfile, join, abspath
import pandas as pd
import sys
import facial_validation_processor as fvp
import warnings
warnings.filterwarnings("ignore")

def import_file(dataset_path):

    #Check format
    if(dataset_path.endswith(('xlsx', 'xls','csv','dta')) is False):
        return (False, 'Supported files are .csv, .dta, .xlsx, .xls')

    # try:
    if dataset_path.endswith(('xlsx', 'xls')):
        dataset = pd.read_excel(dataset_path)
    elif dataset_path.endswith('csv'):
        dataset = pd.read_csv(dataset_path)
    elif dataset_path.endswith('dta'):
        try:
            dataset = pd.read_stata(dataset_path)
        except ValueError:
            dataset = pd.read_stata(dataset_path, convert_categoricals=False)
        label_dict = pd.io.stata.StataReader(dataset_path).variable_labels()
        try:
            value_label_dict = pd.io.stata.StataReader(dataset_path).value_labels()
        except AttributeError:
            status_message = "No value labels detected. " # Not printed in the app, overwritten later.
    elif dataset_path.endswith('vc'):
        status_message = "**ERROR**: This folder appears to be encrypted using VeraCrypt."
        raise Exception
    elif dataset_path.endswith('bc'):
        status_message = "**ERROR**: This file appears to be encrypted using Boxcryptor. Sign in to Boxcryptor and then select the file in your X: drive."
        raise Exception
    else:
        raise Exception

    # except (FileNotFoundError, Exception):
    #     status_message = '**ERROR**: This path appears to be invalid. If your folders or filename contain colons or commas, try renaming them or moving the file to a different location.'

    return dataset

def get_case_id_from_image_name(url_database_pic_names_to_case_id, picture_second_wave):
    
    #Read file
    df_pic_names_to_case_ids = import_file(url_database_pic_names_to_case_id)

    #Get row for given image url
    df_image = df_pic_names_to_case_ids[df_pic_names_to_case_ids['picture_url']==picture_second_wave]

    #Return value in case_id column
    case_id = df_image['case_id'].iloc[0]
    return case_id

if __name__ == '__main__':

    #To work when running from .exe with arguments
    if(len(sys.argv)==4):
        url_folder_baseline_pics = abspath(sys.argv[1])
        url_folder_second_wave_pics = abspath(sys.argv[2])
        pic_names_to_case_id_file_url = abspath(sys.argv[3])
    else:
        print("Did not give arguments")
        sys.exit()

    print(url_folder_baseline_pics)
    print(url_folder_second_wave_pics)
    print(pic_names_to_case_id_file_url)


    #Make file_pairings df to call analyze_images
    file_pairings = pd.DataFrame(columns= ['Picture baseline', 'Picture second-wave'])

    #For every picture in second_wave, check if it matches with its corresponding in baseline
    
    pictures_second_wave = [f for f in listdir(url_folder_second_wave_pics) if isfile(join(url_folder_second_wave_pics, f))]
    for index, picture_second_wave in enumerate(pictures_second_wave):
        picture_second_wave = join(url_folder_second_wave_pics, picture_second_wave)
        #Get case id for this picture
        case_id = get_case_id_from_image_name(pic_names_to_case_id_file_url, picture_second_wave)

        #Get url of picture in baseline
        picture_baseline = url_folder_baseline_pics +'\\'+case_id+'.jpg' #We sure they will all be .jpg?
  
        #Save in df
        file_pairings.loc[index] = [picture_baseline, picture_second_wave]


    status, file_pairings = fvp.process_images(file_pairings)

    status, file_pairings = fvp.compare_images(file_pairings)

    #Save result
    file_pairings.to_csv('results.csv', index=False)