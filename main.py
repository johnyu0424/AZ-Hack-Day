import cv2
import numpy
from PIL import Image, ImageDraw, ImageFilter

def main():

    imgName = "images/park1.jpg"
    coordsList = [
    [(8,10), (8,200), (83,200), (83,10)],
    [(83,10), (83,200), (154,200), (154,10)],
    [(154,10), (154,200), (228,200), (228,10)],
    ]

    '''imgName = "images/bean.png"
    coordsList = [
    [(0,0), (0,200), (200,200), (200,0)],
    [(0,200), (0,400), (200,400), (200,200)],
    [(200,200), (200,400), (400,400), (400,200)],
    ]'''
    
    parking = ProcessParking(imgName, coordsList)
    count = 0
    for spot in parking:
        if spot > .008:
            print('spot %d is OCCUPIED %f' % (count, spot))
        else:
            print('spot %d is OPEN - %f' % (count, spot))
        count+= 1


def ProcessParking(imgName, coordsList):
    # read image as RGB and add alpha (transparency)
    #im = Image.open(imgName).convert("RGBA")
    cvIm = cv2.imread(imgName)

    i = 0
    parkingArray = numpy.zeros(len(coordsList))
    for key in coordsList:
        #tempCroppedImgName = cropImg(i, im, coords)
        tempCroppedImgName = cvCropImg(i,cvIm, coordsList[key])
        #todo: check if cropped image is occupied.
        #Gradient(i, tempCroppedImgName)
        occupiedRatio = ParkingData(i,tempCroppedImgName)
        print (occupiedRatio)
        parkingArray[i] = occupiedRatio
        i+=1
    return parkingArray

def ParkingData(index,sub_imName):
    image = cv2.imread(sub_imName, -1)
    edges = cv2.Canny(image,100,200)
    print(edges)

    edgeImgName = "images/cropped/edges%s.png" % (index)
    cv2.imwrite(edgeImgName, edges)

    # number of white pixels
    numberOfWhitePix = len(numpy.nonzero(edges)[0])
    ratio = numberOfWhitePix / (edges.shape[0] * edges.shape[1])
    return ratio

def cvCropImg(index, im, coords):
    imArray = numpy.asarray(im)

    polygon = [coords[0], coords[1], coords[2], coords[3]]
    # polygon = coords
    maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
    ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
    mask = numpy.array(maskIm)

    cropImg = cv2.bitwise_and(im, im, mask = mask)
    cropImgName = "images/cropped/crp%s.png" % (index)
    cv2.imwrite(cropImgName, cropImg)
    return cropImgName

def cropImg(index, im, coords):
    # convert to numpy (for convenience)
    imArray = numpy.asarray(im)

    # create mask
    #print("%s,%s,%s,%s" % (coords[0], coords[1], coords[2], coords[3]))
    polygon = [coords[0], coords[1], coords[2], coords[3]]
    maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
    ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
    mask = numpy.array(maskIm)

    #mask = mask[:, :, ::-1].copy()
    cv2.cvtColor(mask, cv2.CV_BGR2RGB)
    aImg = cv2.bitwise_and(im, mask)
    aImgName = "images/cropped/aImg%s.png" % (index)
    cv2.imwrite(aImgName, aImg)

    # assemble new image (uint8: 0-255)
    newImArray = numpy.empty(imArray.shape,dtype='uint8')

    # colors (three first columns, RGB)
    newImArray[:,:,:3] = imArray[:,:,:3]

    # transparency (4th column)
    newImArray[:,:,3] = mask*255

    # back to Image from numpy
    newIm = Image.fromarray(newImArray, "RGBA")
    croppedName = "images/cropped/imCropped%s.png" % (index)
    newIm.save(croppedName)
    return croppedName


# if __name__ == "__main__":main() ## with if
