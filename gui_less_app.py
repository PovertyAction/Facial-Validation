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


def get_case_id_from_image_name(survey_path, midline_pic_path):

    #Read survey
    survey_df = import_file(survey_path)

    #Get row for given image url
    df_image = survey_df[survey_df['picture_url']==midline_pic_path]

    #Return value in case_id column
    case_id = df_image['case_id'].iloc[0]
    return case_id

def main(baseline_pics_dir_path, midline_pics_dir_path, survey_path, pic_files_extension='.JPG'):
   # survey.dta aregument is given when midline pics names is not their case id, survey.dta is use to get their caseid

   #Make file_pairings df to call analyze_images
   file_pairings = pd.DataFrame(columns= ['Picture baseline', 'Picture midline'])

   #Generate path to pictures in midline

   midline_pics_names = [f for f in listdir(midline_pics_dir_path) if isfile(join(midline_pics_dir_path, f))]

   #For every picture in midline, check if it matches with its corresponding in baseline
   for index, midline_pic_name in enumerate(midline_pics_names):
       midline_pic_path = join(midline_pics_dir_path, midline_pic_name)

       #If midline_pic caseid is not present in file name, get get case id from survey
       if survey_path:
           baseline_pic_name = get_case_id_from_image_name(survey_path, midline_pic_path)+ pic_files_extension
       else:
           baseline_pic_name = midline_pic_name

       #Get url of picture in baseline
       baseline_pic_path = baseline_pics_dir_path +'\\'+baseline_pic_name

       #Save in df
       file_pairings.loc[index] = [baseline_pic_path, midline_pic_path]

   file_pairings.to_csv('a.csv', index=False)
   print(file_pairings)
   
   status, file_pairings = fvp.process_images(file_pairings)
   file_pairings.to_csv('b.csv', index=False)

   print(file_pairings)
   #
   status, file_pairings = fvp.compare_images(file_pairings)
   #
   # #Save result
   print('e')
   file_pairings.to_csv('results.csv', index=False)

if __name__ == '__main__':

    #If no arguments given, use default for testing
    if(len(sys.argv)==1):
        print("Using default folder locations")
        baseline_pics_dir_path = "C:\\Users\\felip\\Desktop\\GYS Pictures\\GYS Pictures_baseline\\test"
        midline_pics_dir_path = "C:\\Users\\felip\Desktop\\GYS Pictures\\GYS Pictures_midline\\test"
        survey_path = None
    #To work when running from .exe with arguments
    if(len(sys.argv)>=3):
        baseline_pics_dir_path = abspath(sys.argv[1])
        midline_pics_dir_path = abspath(sys.argv[2])

        if(len(sys.argv)==4):
            survey_path = abspath(sys.argv[3])
        else:
            survey_path = None

    main(baseline_pics_dir_path, midline_pics_dir_path, survey_path)
