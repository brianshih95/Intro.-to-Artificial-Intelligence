import os
import cv2

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")
    """
    1. Create a list 'dataset' to store the data of all images
    2. Use 'os.path.join()' to get the path of face and non-face folders
    3. Use 'os.listdir()' to get all files in the folder
    4. Use 'cv2.imread()' to read the image and 
        use 'cv2.IMREAD_GRAYSCALE' to convert to greyscale
    5. If current path is 'face', the second element will be 1.
        Otherwise, 0.
    6. Finally, add the tuple to the 'dataset'
    """
    dataset = []
    path = os.path.join(dataPath, 'face')
    files = os.listdir(path)
    for file in files:
      img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)
      dataset.append((img, 1))
    
    path = os.path.join(dataPath, 'non-face')
    files = os.listdir(path)
    for file in files:
      img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)
      dataset.append((img, 0))
    # End your code (Part 1)
    return dataset
