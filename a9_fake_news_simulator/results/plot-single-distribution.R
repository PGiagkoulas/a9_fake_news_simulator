library(reshape)

#### HOW TO RUN ####
# change the setwd to the directory that stores the 100 sim_runs files and run the whole thing
# you can change the size of elements in the graph at the end of this script to fit your size requirrements
####################
setwd("/Users/sharbatc/Desktop/msc-project-master/dmas/DMAS/CMO/CMO_CLUSTER_SIMPLE/CMO_CLUSTER_SIMPLE_STEPWISE")

# need 1df for pos, 1df for neg
totalFiles = 100

library(mefa)

numRowsVector <- vector()

# timesteps can dynamically change based on when the runs converged

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

# use only reshape package with this, NOT reshape2!
meltposNum <- melt(posNum, id.vars = "runid", measure.vars = timestepvector)
meltposNum$Opinion <- "Positive (+1)"
meltnegNum <- melt(negNum, id.vars = "runid", measure.vars = timestepvector)
meltnegNum$Opinion <- "Negative (-1)"

meltAll <- rbind(meltposNum, meltnegNum)

########### avg summary stuff ##########
library(Rmisc)

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

library(ggplot2)

title = expression(paste("Time step / 10\U00B2", sep = ""))  

p <- ggplot(summarydf, aes(x=variable, y=value, group=Opinion, color=Opinion)) + 
  geom_line() +
  geom_point() +
  geom_errorbar(aes(ymin=value-sd, ymax=value+sd)) +
  scale_x_continuous(breaks = round(seq(0, 55, by = 2))) +
  scale_y_continuous(breaks = round(seq(0, 100, by = 10))) +
  geom_vline(xintercept = avgStop, size = 2) +
  geom_vline(xintercept = avgStop - sdStop, linetype="longdash", size = 1.5) +
  geom_vline(xintercept = avgStop + sdStop, linetype="longdash", size = 1.5) +
  theme(axis.title = element_text(size = 40),
        axis.title.x = element_text(margin = margin(t = 20, r = 0, b = 0, l = 0)),
        axis.title.y = element_text(margin = margin(t = 0, r = 20, b = 0, l = 0)),
        axis.text = element_text(size = 30),
        legend.position = c(0.07, 0.9),
        legend.text = element_text(size = 28),
        axis.ticks = element_line(size = 2),
        legend.title = element_text(size = 33),
        plot.title = element_text(size = 48, hjust = 0.5, margin = margin(t=5, b=20, r=0, l=0))) +
  ylab("No. of agents") +
  xlab(title) +
  scale_color_manual(values = c("#990000", "#336600")) +
  ggtitle("Experiment: CMO and Simple on a Cluster Graph") +
  expand_limits(x = 55, y = 100)
p