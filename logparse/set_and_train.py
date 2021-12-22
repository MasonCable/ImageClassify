import requests, random, cv2, os, time, shutil
import boto3
from pytube import YouTube
from creds import AWS_ACCESS_KEY_ID, AWS_BUCKET, AWS_DEFAULT_REGION, AWS_SECRET_ACCESS_KEY

class SetAndTran():
    """
        This class is used when a new log is created
        #############################################
        1.) Break down the youtube video into images
        2.) Delete the youtube video from storage
        3.) Store images locally in a /testing folder
        4.) Get training images for $game and train against images in /testing
        5.) If the video log is confirmed, store images from video as training data.        
    """

    def __init__(self, videoLink, gameTitle):
        self.videoLink = videoLink
        self.gameTitle = gameTitle
        self.outputFolder = ''

    
    # Take a video link and store images
    def parseVideo(self):
        video = YouTube(self.videoLink)
        # Download the video
        videoTitle = '{}.mp4'.format(self.games)
        video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filename=videoTitle)

        inputFile = videoTitle
        print('{} Created! \n'.format(inputFile))
        outputFolder = 'testing'
        self.outputFolder = outputFolder
        # How many images do we want to store from video
        pictureCount = 20
        step = video.length / pictureCount
        framesCount = video.length

        currentframe = 0
        framesCaptured = 0

        # Try and create the testing folder
        try:
            if not os.path.exists(outputFolder):
                os.makedirs(outputFolder)

        # If the folder can not be created
        except OSError:
            print('Error! Could not create the folder: {}'.format(outputFolder))
        
        # Read the video contents from specified path
        cam = cv2.VideoCapture(inputFile)

        # Read number of frames at particular second
        framePerSecond = cam.get(cv2.CAP_PROP_FPS)

        while (True):
            ret, frame = cam.read()
            if ret:
                currentframe = 0
                # Saving the frames (screenshot)
                name = './{0}/image{1}.jpg'.format(outputFolder, str(framesCaptured))
                print('Creating... ' + name)

                cv2.imwrite(name, frame)
                framesCaptured += 1

                # Breaking the loop when count is achieved
                if framesCaptured > framesCount-1:
                    ret = False
                
            currentframe += 1
        
            if ret == False:
                break
        
    
        # Release all space and windows once done
        cam.release()
        cv2.destroyAllWindows()
        os.remove(inputFile)

