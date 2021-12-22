import requests, random, cv2, os, time, shutil
import boto3
from pytube import YouTube

# Turn video into array of images stored in ../images
def getVideoImages(link):
    video = YouTube(link)
    # Download the video
    videoTitle = 'video.mp4'
    video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filename=videoTitle)
    
    inputFile = videoTitle
    print('{} Created! \n'.format(inputFile))
    outputFolder = 'images'
    
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