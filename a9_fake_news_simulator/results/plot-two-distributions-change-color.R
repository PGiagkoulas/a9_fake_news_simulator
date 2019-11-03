# saving dimensions: 2 dist (1200x800), 1 dist (1200x600), summary (1200x1000)

library(reshape)
library(mefa)
library(Rmisc)
library(ggplot2)

setwd("/home/manvi/Documents/dmas/new_results/dmas/CSV/SYO_CLUSTER_SIMPLE")

totalFiles = 100

numRowsVector <- vector()

# loop to find maximum of convergence points
fileCount = 1
while (fileCount < totalFiles + 1) {
  if (fileCount == 1) {
    filename <- paste("sim_runs_", toString(fileCount), ".csv", sep="")
    newData <- read.csv(filename)
    numRows <- nrow(newData)
    numRowsVector <- c(numRowsVector, numRows)
  }
  else {
    filename <- paste("sim_runs_", toString(fileCount), ".csv", sep="")
    newData <- read.csv(filename)
    numRows <- nrow(newData)
    numRowsVector <- c(numRowsVector, numRows)
  }
  fileCount <- fileCount + 1
}

avgStopDis1 <- mean(numRowsVector) / 10
sdStopDis1 <- sd(numRowsVector) / 10

timesteps = max(numRowsVector, na.rm = TRUE)

timestepvector <- c(1:timesteps)
timestepvector <- paste(timestepvector)

fileCount = 1
while (fileCount < totalFiles + 1) {
  if (fileCount == 1) {
    filename <- paste("sim_runs_", toString(fileCount), ".csv", sep="")
    newData <- read.csv(filename)
    numRows <- nrow(newData)
    if (numRows < timesteps) {
      diffRows <- timesteps - numRows
      appenddf <- rep(tail(newData, 1), times=diffRows)
      newData <- rbind(newData, appenddf)
    }
    extractData <- data.frame(pos = newData$X.positives,
                              neg = newData$X.negatives)
    posNum <- data.frame(t(extractData$pos))
    colnames(posNum) <- timestepvector
    negNum <- data.frame(t(extractData$neg))
    colnames(negNum) <- timestepvector
  }
  else {
    filename <- paste("sim_runs_", toString(fileCount), ".csv", sep="")
    newData <- read.csv(filename)
    numRows <- nrow(newData)
    if (numRows < timesteps) {
      diffRows <- timesteps - numRows
      appenddf <- rep(tail(newData, 1), times=diffRows)
      newData <- rbind(newData, appenddf)
    }
    extractData <- data.frame(pos = newData$X.positives,
                              neg = newData$X.negatives)
    extractPos <- data.frame(t(extractData$pos))
    colnames(extractPos) <- timestepvector
    extractNeg <- data.frame(t(extractData$neg))
    colnames(extractNeg) <- timestepvector
    posNum <- rbind(posNum, extractPos)
    negNum <- rbind(negNum, extractNeg) 
  }
  fileCount <- fileCount + 1
}

posNum$runid <- c(1:totalFiles)
negNum$runid <- c(1:totalFiles)

meltposNum <- melt(posNum, id.vars = "runid", measure.vars = timestepvector)
meltposNum$Opinion <- "Positive (+1) / SYO"
meltnegNum <- melt(negNum, id.vars = "runid", measure.vars = timestepvector)
meltnegNum$Opinion <- "Negative (-1) / SYO"

meltDis1 <- rbind(meltposNum, meltnegNum)

setwd("/home/manvi/Documents/dmas/new_results/dmas/CSV/ANY_CLUSTER_SIMPLE")

totalFiles = 100

numRowsVector <- vector()

# loop to find maximum of convergence points
fileCount = 1
while (fileCount < totalFiles + 1) {
  if (fileCount == 1) {
    filename <- paste("sim_runs_", toString(fileCount), ".csv", sep="")
    newData <- read.csv(filename)
    numRows <- nrow(newData)
    numRowsVector <- c(numRowsVector, numRows)
  }
  else {
    filename <- paste("sim_runs_", toString(fileCount), ".csv", sep="")
    newData <- read.csv(filename)
    numRows <- nrow(newData)
    numRowsVector <- c(numRowsVector, numRows)
  }
  fileCount <- fileCount + 1
}

timesteps = max(numRowsVector, na.rm = TRUE)

timestepvector <- c(1:timesteps)
timestepvector <- paste(timestepvector)

fileCount = 1
while (fileCount < totalFiles + 1) {
  if (fileCount == 1) {
    filename <- paste("sim_runs_", toString(fileCount), ".csv", sep="")
    newData <- read.csv(filename)
    numRows <- nrow(newData)
    if (numRows < timesteps) {
      diffRows <- timesteps - numRows
      appenddf <- rep(tail(newData, 1), times=diffRows)
      newData <- rbind(newData, appenddf)
    }
    extractData <- data.frame(pos = newData$X.positives,
                              neg = newData$X.negatives)
    posNum <- data.frame(t(extractData$pos))
    colnames(posNum) <- timestepvector
    negNum <- data.frame(t(extractData$neg))
    colnames(negNum) <- timestepvector
  }
  else {
    filename <- paste("sim_runs_", toString(fileCount), ".csv", sep="")
    newData <- read.csv(filename)
    numRows <- nrow(newData)
    if (numRows < timesteps) {
      diffRows <- timesteps - numRows
      appenddf <- rep(tail(newData, 1), times=diffRows)
      newData <- rbind(newData, appenddf)
    }
    extractData <- data.frame(pos = newData$X.positives,
                              neg = newData$X.negatives)
    extractPos <- data.frame(t(extractData$pos))
    colnames(extractPos) <- timestepvector
    extractNeg <- data.frame(t(extractData$neg))
    colnames(extractNeg) <- timestepvector
    posNum <- rbind(posNum, extractPos)
    negNum <- rbind(negNum, extractNeg) 
  }
  fileCount <- fileCount + 1
}

posNum$runid <- c(1:totalFiles)
negNum$runid <- c(1:totalFiles)

meltposNum <- melt(posNum, id.vars = "runid", measure.vars = timestepvector)
meltposNum$Opinion <- "Positive (+1) / no SYO"
meltnegNum <- melt(negNum, id.vars = "runid", measure.vars = timestepvector)
meltnegNum$Opinion <- "Negative (-1) / no SYO"

meltDis2 <- rbind(meltposNum, meltnegNum)

meltAll <- rbind(meltDis2, meltDis1)

meltAll$Opinion <- as.factor(meltAll$Opinion)

summarydf <- summarySE(meltAll,
                       measurevar="value",
                       groupvars=c("variable", "Opinion"))

# make the summarydf smaller bcoz no space to plot
# rowsToRemove = setdiff(1:timesteps,seq(1,timesteps,20))
# summarydf <- summarydf[-rowsToRemove, ]

# change variable to numeric from factor
summarydf$variable <- as.numeric(levels(summarydf$variable))[summarydf$variable]
summarydf$variable <- summarydf$variable / 10

avgStop <- mean(numRowsVector) / 10
sdStop <- sd(numRowsVector) / 10

title = expression(paste("Time step / 10\U00B2", sep = ""))

oldavgStop <- avgStopDis1
oldsdStop <- sdStopDis1

p <- ggplot(summarydf, aes(x=variable, y=value, color=Opinion)) + 
  geom_line() +
  geom_point() +
  geom_errorbar(aes(ymin=value-sd, ymax=value+sd)) +
  scale_x_continuous(breaks = round(seq(0, 525, by = 25))) +
  scale_y_continuous(breaks = round(seq(0, 100, by = 10))) +
  geom_vline(xintercept = avgStop, size = 1.2, alpha = 0.5) +
  geom_vline(xintercept = avgStop - sdStop, linetype="longdash", size = 1, alpha = 0.5) +
  geom_vline(xintercept = avgStop + sdStop, linetype="longdash", size = 1, alpha = 0.5) +
  geom_vline(xintercept = oldavgStop, size = 1.2, alpha = 0.8) +
  geom_vline(xintercept = oldavgStop - oldsdStop, linetype="longdash", size = 1, alpha = 0.8) +
  geom_vline(xintercept = oldavgStop + oldsdStop, linetype="longdash", size = 1, alpha = 0.8) +
  theme(axis.title = element_text(size = 23),
        axis.title.x = element_text(margin = margin(t = 10)),
        axis.title.y = element_text(margin = margin(r = 10)),
        axis.text = element_text(size = 18),
        legend.position = c(0.35, 0.45),
        legend.text = element_text(size = 15),
        axis.ticks = element_line(size = 1.5),
        legend.title = element_text(size = 17)) +
  ylab("No. of agents") +
  xlab(title) +
  scale_color_manual(values = c( "#E74C3C", "#990000", "#2ECC71", "#336600")) +
  expand_limits(x = 525, y = 100)
#  guides(alpha=FALSE)
p

