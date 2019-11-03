library(reshape)
library(mefa)
library(Rmisc)
library(ggplot2)

do_stuff <- function(wdName, protocolName) {
  setwd(wdName)
  
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
  
  avgStopDis <- mean(numRowsVector) / 10
  sdStopDis <- sd(numRowsVector) / 10
  
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
  meltposNum$Opinion <- paste("Positive (+1) / ", protocolName, sep = "")
  meltnegNum <- melt(negNum, id.vars = "runid", measure.vars = timestepvector)
  meltnegNum$Opinion <- paste("Negative (-1) ", protocolName, sep = "")
  
  meltDis <- rbind(meltposNum, meltnegNum)
  
  return_list <- list("avgStop" = avgStopDis,
                      "sdStop" = sdStopDis,
                      "returnDf" = meltDis)
  
  return(return_list)
}

############## Distribution 1 ####################

returned_things <- do_stuff("/home/manvi/Documents/dmas/new_results/dmas/CSV/CMO_RANDOM_DISCUSSION", "CMO / LNS")

avgStopDis1 <- returned_things[1]
sdStopDis1 <- returned_things[2]
meltDis1 <- returned_things[3]

avgStopDis1 <- as.numeric(unlist(avgStopDis1))
sdStopDis1 <- as.numeric(unlist(sdStopDis1))
meltDis1 <- data.frame(meltDis1)

############## Distribution 2 ####################

returned_things <- do_stuff("/home/manvi/Documents/dmas/new_results/dmas/CSV/ANY_RANDOM_DISCUSSION", "ANY")

avgStopDis2 <- returned_things[1]
sdStopDis2 <- returned_things[2]
meltDis2 <- returned_things[3]

avgStopDis2 <- as.numeric(unlist(avgStopDis2))
sdStopDis2 <- as.numeric(unlist(sdStopDis2))
meltDis2 <- data.frame(meltDis2)

############## Distribution 3 ####################

returned_things <- do_stuff("/home/manvi/Documents/dmas/new_results/dmas/CSV/SYO_RANDOM_DISCUSSION", "SYO")

avgStopDis3 <- returned_things[1]
sdStopDis3 <- returned_things[2]
meltDis3 <- returned_things[3]

avgStopDis3 <- as.numeric(unlist(avgStopDis3))
sdStopDis3 <- as.numeric(unlist(sdStopDis3))
meltDis3 <- data.frame(meltDis3)

########## All distributions together ############

meltAll <- rbind(meltDis1, meltDis2, meltDis3)
colnames(meltAll) <- c("runid", "variable", "value", "Opinion")

meltAll$Opinion <- as.factor(meltAll$Opinion)

summarydf <- summarySE(meltAll,
                       measurevar="value",
                       groupvars=c("variable", "Opinion"))

summarydf$variable <- as.numeric(levels(summarydf$variable))[summarydf$variable]
summarydf$variable <- summarydf$variable / 10

title = expression(paste("Time step / 10\U00B2", sep = ""))

p <- ggplot(summarydf, aes(x=variable, y=value, color=Opinion)) + 
  geom_line() +
  geom_point() +
  geom_errorbar(aes(ymin=value-sd, ymax=value+sd)) +
  scale_x_continuous(breaks = round(seq(0, 525, by = 25))) +
  scale_y_continuous(breaks = round(seq(0, 100, by = 10))) +
  geom_vline(xintercept = avgStopDis1, size = 1.2) +
  geom_vline(xintercept = avgStopDis1 - sdStopDis1, linetype="longdash", size = 1) +
  geom_vline(xintercept = avgStopDis1 + sdStopDis1, linetype="longdash", size = 1) +
  geom_vline(xintercept = avgStopDis2, size = 1.2, alpha = 0.4) +
  geom_vline(xintercept = avgStopDis2 - sdStopDis2, linetype="longdash", size = 1, alpha = 0.4) +
  geom_vline(xintercept = avgStopDis2 + sdStopDis2, linetype="longdash", size = 1, alpha = 0.4) +
  geom_vline(xintercept = avgStopDis3, size = 1.2, alpha = 0.1) +
  geom_vline(xintercept = avgStopDis3 - sdStopDis3, linetype="longdash", size = 1, alpha = 0.1) +
  geom_vline(xintercept = avgStopDis3 + sdStopDis3, linetype="longdash", size = 1, alpha = 0.1) +
  theme(axis.title = element_text(size = 23),
        axis.title.x = element_text(margin = margin(t = 10)),
        axis.title.y = element_text(margin = margin(r = 10)),
        axis.text = element_text(size = 18),
        legend.position = c(0.8, 0.45),
        legend.text = element_text(size = 15),
        axis.ticks = element_line(size = 1.5),
        legend.title = element_text(size = 17)) +
  ylab("No. of agents") +
  xlab(title) +
  scale_color_manual(values = c("#F1948A", "#E74C3C", "#990000", "#ABEBC6", "#2ECC71", "#336600")) +
  expand_limits(x = 525, y = 100)
#  guides(alpha=FALSE)
p





