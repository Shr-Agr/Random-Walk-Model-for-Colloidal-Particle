import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

errorData = []
for j in np.arange(1, 15):
    print(j)
    circles_data = []

    maxNumberOfParticles = 0
    minNumberOfParticles = 1000000
    sum = 0
    imageIdContainingMaxNumberOfParticles = 0
    imageIdContainingMinNumberOfParticles = 0

    for i in range(0,490):
        
        imgNumber    = str(i)
        imgNumber    = imgNumber.zfill(5)

        fileLocation = f"C:\\Users\\asus\\Downloads\\images\\images\\Img_{imgNumber}.tif"

        originalImage = cv.imread(fileLocation)
        
        y_coordinate = originalImage.shape[1]
        x_coordinate = originalImage.shape[0]
        
        img = cv.cvtColor(originalImage[0:x_coordinate//j, 0:y_coordinate//j], cv.COLOR_BGR2GRAY)
        
        blur         = cv.GaussianBlur(img, (19, 19), 0)

        threshold    = cv.threshold(blur, 125, 255, cv.THRESH_BINARY)[1]
        
        circles      = cv.HoughCircles(threshold, cv.HOUGH_GRADIENT,
                                        dp=2.8, minDist=13,
                                        param1 = 20, param2 = 10,
                                        minRadius = 1, maxRadius = 7)

        circles_data.append(circles)

        if circles is not None:

            numberOfParticles = circles.shape[1]
            sum += numberOfParticles

            # print("\nNo. of particles in ", imgNumber, "th", "image : ",numberOfParticles)

            if(maxNumberOfParticles < numberOfParticles):

                maxNumberOfParticles = numberOfParticles
                imageIdContainingMaxNumberOfParticles = i

            if(minNumberOfParticles > numberOfParticles):
                
                minNumberOfParticles = numberOfParticles
                imageIdContainingMinNumberOfParticles = i


    print("\nImage Id Containing Max Number Of Particles: ", imageIdContainingMaxNumberOfParticles)
    print("Max Number Of Particles: ", maxNumberOfParticles)
    print("\nImage Id Containing Min Number Of Particles: ", imageIdContainingMinNumberOfParticles)
    print("Min Number Of Particles: ", minNumberOfParticles)


    # Average value of number of circles in all images

    average = (sum / len(circles_data))

    print("\naverage: ", average)


    combinedData = []
    meanData = []

    totalNumberOfParticles = 0
    totalNumberOfImages = len(circles_data)

    for i in range(totalNumberOfImages):
        
        dataOfSingleImage = []
        numberOfParticlesInEachImage = len(circles_data[i][0])
        totalNumberOfParticles += numberOfParticlesInEachImage
        
        for j in range(numberOfParticlesInEachImage):

            Xc = circles_data[i][0][j][0]
            Yc = circles_data[i][0][j][1]
            r  = circles_data[i][0][j][2]
            
            dataOfSingleParticle = [i,Xc,Yc,r]
            combinedData.append( dataOfSingleParticle )
            dataOfSingleImage.append( dataOfSingleParticle )
            
        dfPerImage = pd.DataFrame(dataOfSingleImage, columns = ['Image Number', 'Xc', 'Yc', 'R'])
        meanData.append(list(dfPerImage.mean()))

    dfPopulation      = pd.DataFrame(combinedData , columns = ['Image Number', 'Xc', 'Yc', 'R'])
    dfMean            = pd.DataFrame(meanData     , columns = ['Image Number', 'Mean of Xc', 'Mean of Yc', 'Mean of R'])

    print(dfMean)

    # Expectation value of the mean of x-coordinates = Mean of x-coord. values from dfMean dataframe.
    expectationOfSampleMean = list(dfMean.mean())[1]
    print("\nExpectation value of sample mean(Xc): ", expectationOfSampleMean)

    print(dfMean.std())
    # Standarad Deviation of sample mean (mean of average x-coordinates for the images)
    standardDeviationOfSampleMean = (list(dfMean.var(ddof=0))[1])**0.5
    print("Standarad Deviation of sample mean: ", standardDeviationOfSampleMean)

    # Mean of Population
    populationMean = list(dfPopulation.mean())[1]
    print("\nMean of Population: ", populationMean)


    # Value of "Standard Deviation of divided by n" for the population
    var = list(dfPopulation.var(ddof=0))[1]
    sigma = var**0.5
    print("Standard Deviation of the population divided by sqrt n: ", sigma/(average**0.5))
    print("\n")

    # create a histogram with bins determined by the Freedman-Diaconis' rule
    plt.hist(dfMean['Mean of Xc'], bins='fd')
    plt.show()

    cv.waitKey(0)

    error = ((sigma/(average**0.5)) - standardDeviationOfSampleMean)/(sigma/(average**0.5))
    errorData.append(error)

print(errorData)