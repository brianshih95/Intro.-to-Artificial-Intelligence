import os
import cv2

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    # raise NotImplementedError("To be implemented")
    """
    1. Create 'locations' to store the location and size of each face,
        'filenames' to store the name of each image, 
        and 'line_cnt' to store the number of faces of each image 
    2. Use 'open()' to open 'detectData.txt'
    3. Use 'readlines()' to read in the information line by line
    4. Use 'strip()' to remove any leading and trailing spaces
    5. Use 'split()' to split the line into a list
    6. If the first item in the list is a number, 
        it means that this line is the information about location.
        Otherwise, it is about filename.
    7. Use 'os.path.join()' to get the path of the image
    8. Use 'cv2.imread()' to read the image
    9. Because the image has to be grey when classifying, 
        use 'cv2.IMREAD_GRAYSCALE' to convert it to greyscale
    10. Because we have to draw green and red rectangles in the final result,
        create 'img_ori' to store the original image
    11. Create 'crop_img' to store the cropped image,
        and then resize it to (19, 19)
    12. After trying all of the interpolation methods, 
        'cv2.INTER_NEAREST' perform the best, so I choose it.
    13. If the cropped image is identified as a face, draw a green rectangle on it.
        Otherwise, draw a red one.
    """
    
    GREEN = [0, 255, 0]
    RED = [0, 0, 255]
    
    locations = []
    filenames = []
    line_cnt = []
    
    with open(dataPath, 'r') as f:
      i = 0
      for line in f.readlines():
        line = line.strip()
        strs = line.split(' ')
        if str.isdigit(strs[0]):
          locations.append([])
          for j in range(4):
            locations[i].append(int(strs[j]))
          i += 1
        else:
          filenames.append(strs[0])
          line_cnt.append(int(strs[1]))

    file_cnt = 0
    line_idx = 0
    for line in line_cnt:
      path = os.path.join('data/detect', filenames[file_cnt])
      file_cnt += 1
      img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
      img_ori = cv2.imread(path)
      for _ in range(line):
        x = locations[line_idx][0]
        y = locations[line_idx][1]
        w = locations[line_idx][2]
        h = locations[line_idx][3]
        crop_img = img[y:y+h, x:x+w]
        crop_img = cv2.resize(crop_img, (19, 19), interpolation=cv2.INTER_NEAREST)
        ans = clf.classify(crop_img)
        if ans:
          cv2.rectangle(img_ori, (x, y), (x+w, y+h), GREEN, 2)
        else:
          cv2.rectangle(img_ori, (x, y), (x+w, y+h), RED, 2)
        line_idx += 1
      cv2.imshow('result', img_ori)
      cv2.waitKey(0)
      cv2.destroyAllWindows()
      
    # End your code (Part 4)
