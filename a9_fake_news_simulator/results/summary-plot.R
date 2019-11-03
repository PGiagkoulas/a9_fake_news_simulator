library(ggplot2)
library(reshape)
library(mefa)
library(Rmisc)

totalFiles = 100

gossipProts <- c("CMO", "SYO", "ANY", "LNS")
connectivity <- c("CLUSTER", "RANDOM", "SUN")
interactionProts <- c("SIMPLE", "DISCUSSION", "MAJORITY")

createCombinations <- function(gossipVec, connVec, interVec) {
  returnVec <- vector()
  for (gossipProt in gossipVec) {
    for (connType in connVec) {
      for (interProt in interVec) {
        folderName <- paste(gossipProt, connType, interProt, sep="_")
        returnVec <- c(returnVec, folderName)
      }
    }
  }
  return(returnVec)
}

folderNames <- createCombinations(gossipProts, connectivity, interactionProts)

# folderNames <- c("CMO_CLUSTER_SIMPLE_STEPWISE", "CMO_CLUSTER_MAJORITY_STEPWISE")

runLoop <- function(totalFiles) {
  # loop to find the convergence pts and consensus state points
  # for now , don't know how to deal with consensus states in cases where there are isolated agents
  convergenceVector <- vector()
  consensusVector <- vector()
  fileCount = 1
  while (fileCount < totalFiles + 1) {
    filename <- paste("sim_runs_", toString(fileCount), ".csv", sep="")
    newData <- read.csv(filename)
    newData$totalAgents <- newData$X.positives + newData$X.isolates
    newData$rowNum <- c(1:nrow(newData))
    firstOccVector <- newData[match(95, newData$totalAgents),]
    firstOccNum <- firstOccVector$rowNum
    numRows <- nrow(newData)
    convergenceVector <- c(convergenceVector, numRows)
    consensusVector <- c(consensusVector, firstOccNum)
    fileCount <- fileCount + 1
  }
  vecList <- list("conv" = convergenceVector, "consen" = consensusVector)
  return(vecList)
}

firstElReached <- 0

# print("current working directory:")
# print(getwd())

for (folder in folderNames) {
  wdName <- paste("/Users/sharbatc/Desktop/msc-project-master/dmas/DMAS/", folder, sep = "")
  setwd(wdName)
  # print("set working directory to:")
  # print(getwd())
  if (firstElReached == 0) {
    vecList <- runLoop(totalFiles)
    convVec <- vecList$conv
    convVec[is.na(convVec)] <- 0
    consenVec <- vecList$consen
    consenVec[is.na(consenVec)] <- 0
    
    meanConv <- mean(convVec)
    sdConv <- sd(convVec)
    convDf <- data.frame("meanVal" <- c(meanConv),
                        "sdVal" <- c(sdConv),
                        "protComb" <- c(folder))
    
    meanConsen <- mean(consenVec)
    sdConsen <- sd(consenVec)
    consenDf <- data.frame("meanVal" <- c(meanConsen),
                           "sdVal" <- c(sdConsen),
                           "protComb" <- c(folder))
    # print("Created the new df")
    firstElReached <- 1
  }
  else {
    vecList <- runLoop(totalFiles)
    convVec <- vecList$conv
    convVec[is.na(convVec)] <- 0
    consenVec <- vecList$consen
    consenVec[is.na(consenVec)] <- 0
    
    meanConv <- mean(convVec)
    sdConv <- sd(convVec)
    newconvDf <- data.frame("meanVal" <- c(meanConv),
                         "sdVal" <- c(sdConv),
                         "protComb" <- c(folder))
    
    meanConsen <- mean(consenVec)
    sdConsen <- sd(consenVec)
    newconsenDf <- data.frame("meanVal" <- c(meanConsen),
                           "sdVal" <- c(sdConsen),
                           "protComb" <- c(folder))
    convDf <- rbind(convDf, newconvDf)
    consenDf <- rbind(consenDf, newconsenDf)
    # print("Added the df for this to existing df")
  }
}

colnames(convDf) <- c("meanVal", "sdVal", "protComb")
convDf$Metric <- "Convergence"
colnames(consenDf) <- c("meanVal", "sdVal", "protComb")
consenDf$Metric <- "Consensus"

allDf <- rbind(convDf, consenDf)

allDf$meanVal <- allDf$meanVal / 10

title = expression(paste("Time step / 10\U00B2", sep = ""))

p <- ggplot(allDf, aes(x=protComb, y=meanVal, group=Metric, color=Metric)) + 
  geom_errorbar(aes(ymin=meanVal-sdVal, ymax=meanVal+sdVal), width=.2) +
  geom_line() +
  geom_point(size = 2) +
  ylab(title) +
  xlab("Protocol Combination") +
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5),
        legend.position = c(0.1,0.8),
        axis.title = element_text(size = 23),
        axis.text = element_text(size = 18),
        legend.title = element_text(size = 17),
        legend.text = element_text(size = 15),
        axis.title.x = element_text(margin = margin(t = 10)),
        axis.title.y = element_text(margin = margin(r = 10))) +
  scale_y_continuous(breaks = round(seq(0, 5500, by = 250)))
p
