# import matplotlib.pyplot as plt
import numpy as np
import os, boto3, random, cv2, shutil, pathlib
from creds import AWS_ACCESS_KEY_ID, AWS_BUCKET, AWS_DEFAULT_REGION, AWS_SECRET_ACCESS_KEY

# import PIL
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from tensorflow.keras.models import Sequential



class Train():    
    def __init__(self, game):
        self.game = game

    def getImages(self):
        s3 = boto3.client('s3', AWS_DEFAULT_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        # bucket = s3.Bucket(AWS_BUCKET)['Contents']
        imgCount = []
        pathName = 'games/training/{}'.format(self.game)
        for key in s3.list_objects(Bucket=AWS_BUCKET)['Contents']:
            if pathName in key['Key'] and len(imgCount) <= 20 :
                fileName = key['Key'].split("{}/".format(pathName),1)[1]						
                imgCount.append(key)
                try:  
                    # creating a folder named data 
                    if not os.path.exists('images'): 
                        os.makedirs('images') 
                
                #if not created then raise error 
                except OSError: 
                    print ('Error! Could not create a directory') 
                
                print('Downloading: {} ...'.format(fileName))
                s3.download_file(AWS_BUCKET, key['Key'], './images/'+fileName)
                
            
        if len(imgCount) == 0:
            print('No files were found in games/training/{}'.format(self.game))
        else:
            print('Training images succesfully downloaded \n')
    

    
        