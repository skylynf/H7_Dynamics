setwd("E:/qinliugan/H7/H7N9/beast/continuous/host/anser")
install.packages("devtools"); library(devtools)
install_github("sdellicour/seraphim/unix_OS") # for Unix systems
install_github("sdellicour/seraphim/windows") # for Windows systems
rm(list = ls())
library(seraphim)


# 1. Extracting spatio-temporal information embedded in trees

localTreesDirectory = "Extracted_trees"
allTrees = scan(file="H7N9anser.trees", what="", sep="\n", quiet=TRUE)
burnIn = 0
randomSampling = FALSE
nberOfTreesToSample = 100
mostRecentSamplingDatum = 2021.02
coordinateAttributeName = "location"


treeExtractions(localTreesDirectory, allTrees, burnIn, randomSampling, 
                nberOfTreesToSample, mostRecentSamplingDatum, coordinateAttributeName)

?treeExtractions()
# 2. Estimation of several dispersal statistics

nberOfExtractionFiles = 100
timeSlices = 100
onlyTipBranches = FALSE
showingPlots = FALSE
outputName = "WNV"
nberOfCores = 1
slidingWindow = 1
simulations=FALSE

spreadStatistics(localTreesDirectory, nberOfExtractionFiles, timeSlices, onlyTipBranches, 
                 showingPlots, outputName, nberOfCores, slidingWindow,simulations=FALSE)

getAnywhere(treeExtractions)
list.files("Extracted_trees")
lines <- readLines("WNV_gamma.trees", n = 10)
print(lines)
if (!dir.exists("Extracted_trees")) {
  dir.create("Extracted_trees")
}
result <- treeExtractions(localTreesDirectory, allTrees, burnIn, randomSampling, 
                          nberOfTreesToSample, mostRecentSamplingDatum, coordinateAttributeName)
print(result)
dir.exists(localTreesDirectory)
