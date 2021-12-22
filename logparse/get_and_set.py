import requests, random, cv2, os, time, shutil
import boto3
from pytube import YouTube
from creds import AWS_ACCESS_KEY_ID, AWS_BUCKET, AWS_DEFAULT_REGION, AWS_SECRET_ACCESS_KEY

class GetAndSet():    
    """
        We Need a video link and video type to determine 
        how to handle the parsing
    """
    def __init__(self, link, videoType, gameTitle):
        self.link = link
        self.videoType = videoType
        self.gameTitle = gameTitle
        self.outputFolder = ''
    
    # Given a video link we need to get the timestamp model built
    def generateTimestampObj(self):
        """
            %% DEPRECATED FOR RIGHT NOW %%
            This function splits the video into thirds and grabs random
            timestamps from each section.
        """
        video = YouTube(self.link)
        videoLength = video.length
        den = 1
        partsCount = 3
        part = videoLength / partsCount

        start = part
        xStart = [random.randint(0, start) for p in range(10)]
        middle = start + part
        xMiddle = [random.randint(start + den, middle) for p in range(10)]
        end = middle + part
        xEnd = [random.randint(middle + den, end) for p in range(10)]

        tsObj = {
            'start': xStart,
            'middle': xMiddle,
            'end': xEnd
        }

        print(tsObj)

    # Turn video into array of images stored in ../images
    def getVideoImages(self):
        video = YouTube(self.link)
        # Download the video
        videoTitle = 'video.mp4'
        video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filename=videoTitle)
        
        inputFile = videoTitle
        print('{} Created! \n'.format(inputFile))
        outputFolder = 'images'
        self.outputFolder = outputFolder
        pictureCount = 20
        step = video.length / pictureCount
        frames_count = video.length

        currentframe = 0
        frames_captured = 0

        #creating a folder
        try:  
            # creating a folder named data 
            if not os.path.exists(outputFolder): 
                os.makedirs(outputFolder) 
            
        #if not created then raise error 
        except OSError: 
            print ('Error! Could not create a directory') 

        #reading the video from specified path 
        cam = cv2.VideoCapture(inputFile) 
        
        #reading the number of frames at that particular second
        frame_per_second = cam.get(cv2.CAP_PROP_FPS)

        while (True):
            ret, frame = cam.read()
            if ret:
                if currentframe > (step*frame_per_second):  
                    currentframe = 0
                    #saving the frames (screenshots)
                    name = './{0}/image{1}.jpg'.format(outputFolder, str(frames_captured))
                    print ('Creating...' + name ) 
                    
                    cv2.imwrite(name, frame)       
                    frames_captured+=1
                    
                    #breaking the loop when count achieved
                    if frames_captured > frames_count-1:
                        ret = False
                currentframe += 1           
            if ret == False:
                break

        #Releasing all space and windows once done
        cam.release()
        cv2.destroyAllWindows()
        os.remove(inputFile)
        
    
    def start(self):
        print('Reading the video and generating training data...\n')
                    
        self.getVideoImages()
        print('Video read and parsed! \n')
            
        
        s3StorePath = '/games/training/{}/'.format(self.gameTitle)
        print('storing the images in S3 with the following key: {}\n'.format(s3StorePath))
        self.uploadImagesToS3()

	
    def uploadImagesToS3(self):
        s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        bucket = s3.Bucket(AWS_BUCKET)

        # Get the path to upload to or create it
        basePath = 'games/training/{}/'.format(self.gameTitle)        
                        
        try:
            for root, dirs, files in os.walk('images'):
                for file in files:
                    print('{}\n'.format(root))
                    print('Uploading {} to {} ...'.format(file, basePath+file))
                    s3.Bucket(AWS_BUCKET).upload_file(os.path.join(root, file), basePath+file)
            print('All Files were succesfully uploaded')

        except:
            print("There was an error ")
        
        # Remove the video file
        dir_path = './{}'.format('images')
        try:
            print('Deleting the Images folder from local machine')
            shutil.rmtree(dir_path)
        except OSError as e:
        	print("Error: %s : %s" % (dir_path, e.strerror))

   




        

        


                
                    
                    