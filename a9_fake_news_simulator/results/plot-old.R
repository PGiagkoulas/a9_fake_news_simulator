library(tidyverse)
library("ggplot2")

setwd("/home/manvi/Documents/dmas/results")

df1 <- read.csv("sim_runs_10.csv")
df2 <- read.csv("sim_runs_11.csv")
df3 <- read.csv("sim_runs_12.csv")
df4 <- read.csv("sim_runs_13.csv")
df5 <- read.csv("sim_runs_14.csv")
df6 <- read.csv("sim_runs_15.csv")
df7 <- read.csv("sim_runs_16.csv")
df8 <- read.csv("sim_runs_17.csv")
df9 <- read.csv("sim_runs_18.csv")


make_basicdf <- function(datadf) {
  return_basicdf <- data.frame(timestep = datadf$current.step,
                               pos = datadf$X.positives,
                               neg = datadf$X.negatives,
                               neut = datadf$X.neutrals)
  return(return_basicdf)
}

make_plotdf <- function(datadf) {
  return_plotdf <- datadf %>%
    select(timestep, pos, neg, neut) %>%
    gather(key = "variable", value = "value", -timestep)
  return(return_plotdf)
}

make_plot <- function(datadf) {
  return_plot <- ggplot(datadf, aes(x = timestep, y = value)) +
    geom_line(aes(color=variable))
  return(return_plot)
}

###### Individual dataframes #########

any_disc <- make_basicdf(df1)
any_disc_plotdf <- make_plotdf(any_disc)

any_maj <- make_basicdf(df2)
any_maj_plotdf <- make_plotdf(any_maj)

any_simple <- make_basicdf(df3)
any_simple_plotdf <- make_plotdf(any_simple)

syo_disc <- make_basicdf(df4)
syo_disc_plotdf <- make_plotdf(syo_disc)
  
syo_maj <- make_basicdf(df5)
syo_maj_plotdf <- make_plotdf(syo_maj)
  
syo_simple <- make_basicdf(df6)
syo_simple_plotdf <- make_plotdf(syo_simple)
  
cmo_disc <- make_basicdf(df7)
cmo_disc_plotdf <- make_plotdf(cmo_disc)

cmo_maj <- make_basicdf(df8)
cmo_maj_plotdf <- make_plotdf(cmo_maj)
  
cmo_simple <- make_basicdf(df9)
cmo_simple_plotdf <- make_plotdf(cmo_simple)

######## Plot individual data frames ########3

any_disc_plot <- make_plot(any_disc_plotdf)

any_disc_plot

any_maj_plot <- make_plot(any_maj_plotdf)

any_maj_plot

any_simple_plot <- make_plot(any_simple_plotdf)

any_simple_plot

syo_disc_plot <- make_plot(syo_disc_plotdf)

syo_disc_plot

syo_maj_plot <- make_plot(syo_maj_plotdf)

syo_maj_plot

syo_simple_plot <- make_plot(syo_simple_plotdf)

syo_simple_plot

cmo_disc_plot <- make_plot(cmo_disc_plotdf)

cmo_disc_plot

cmo_maj_plot <- make_plot(cmo_maj_plotdf)

cmo_maj_plot

cmo_simple_plot <- make_plot(cmo_simple_plotdf)

cmo_simple_plot

###### Runs dataframes #########

df1 <- read.csv("sim_runs_1.csv")
df2 <- read.csv("sim_runs_2.csv")
df3 <- read.csv("sim_runs_3.csv")
df4 <- read.csv("sim_runs_4.csv")
df5 <- read.csv("sim_runs_5.csv")
df6 <- read.csv("sim_runs_6.csv")
df7 <- read.csv("sim_runs_7.csv")
df8 <- read.csv("sim_runs_8.csv")
df9 <- read.csv("sim_runs_9.csv")

make_basicdf_runs <- function(datadf, groupstr) {
  pos_df <- data.frame(val = datadf$X.positives)
  pos_df$Opinion <- "+1"
  neg_df <- data.frame(val = datadf$X.negatives)
  neg_df$Opinion <- "-1"
  return_basicdf_runs <- rbind(pos_df, neg_df)
  return_basicdf_runs$prot <- groupstr
  return(return_basicdf_runs)
}
combinedf <- function(datadf1, datadf2, datadf3) {
  return_df <- rbind(datadf1, datadf2, datadf3)
}
makeplot <- function(datadf) {
  p <- ggplot(datadf, aes(x=prot, y=val, fill=Opinion)) +
    geom_dotplot(binaxis='y', stackdir='center', dotsize=0.6,
                 position=position_dodge(0.5),
                 binwidth = 2.5) +
    scale_y_continuous(breaks = c(0,10,20,30,40,50,60,70,80,90,100)) +
    theme(axis.title = element_text(size=30),
          axis.text = element_text(size=20),
          legend.text = element_text(size=15),
          legend.title = element_text(size = 20)) +
    xlab("Protocol Combination") +
    ylab("Number of Agents") +
    scale_x_discrete(labels=c("any_disc" = "ANY \n + Disc", "any_maj" = "ANY \n + Maj",
                              "any_simple" = "ANY \n + Conv", "cmo_disc" = "CMO \n + Disc",
                              "cmo_maj"= "CMO \n + Maj", "cmo_simple" = "CMO \n + Conv",
                              "syo_disc" = "SYO \n + Disc", "syo_maj" = "SYO \n + Maj",
                              "syo_simple" = "SYO \n + Conv"))
  return(p)
}
makeplot_wo_legend <- function(datadf) {
  p <- ggplot(datadf, aes(x=prot, y=val, fill=Opinion)) +
    geom_dotplot(binaxis='y', stackdir='center', dotsize=0.6,
                 position=position_dodge(0.5),
                 binwidth = 2.5) +
    scale_y_continuous(breaks = c(0,10,20,30,40,50,60,70,80,90,100)) +
    theme(axis.title = element_text(size=30),
          axis.text = element_text(size=20),
          legend.position = "none") +
    xlab("Protocol Combination") +
    ylab("Number of Agents") +
    scale_x_discrete(labels=c("any_disc" = "ANY \n + Disc", "any_maj" = "ANY \n + Maj",
                              "any_simple" = "ANY \n + Conv", "cmo_disc" = "CMO \n + Disc",
                              "cmo_maj"= "CMO \n + Maj", "cmo_simple" = "CMO \n + Conv",
                              "syo_disc" = "SYO \n + Disc", "syo_maj" = "SYO \n + Maj",
                              "syo_simple" = "SYO \n + Conv"))
  return(p)
}

any_disc <- make_basicdf_runs(df1, "any_disc")
any_maj <- make_basicdf_runs(df2, "any_maj")
any_simple <- make_basicdf_runs(df3, "any_simple")
any_df <- combinedf(any_disc, any_maj, any_simple)
any_plot <- makeplot(any_df)

syo_disc <- make_basicdf_runs(df4, "syo_disc")
syo_maj <- make_basicdf_runs(df5, "syo_maj")
syo_simple <- make_basicdf_runs(df6, "syo_simple")
syo_df <- combinedf(syo_disc, syo_maj, syo_simple)
syo_plot <- makeplot(syo_df)

cmo_disc <- make_basicdf_runs(df7, "cmo_disc")
cmo_maj <- make_basicdf_runs(df8, "cmo_maj")
cmo_simple <- make_basicdf_runs(df9, "cmo_simple")
cmo_df <- combinedf(cmo_disc, cmo_maj, cmo_simple)
cmo_plot <- makeplot(cmo_df)

all_df <- combinedf(any_df, syo_df, cmo_df)
all_plot <- makeplot_wo_legend(all_df)
all_plot

######## plotting avg and std of 100 runs ###########
library(reshape)

setwd("/home/manvi/Documents/dmas/sun_CMO_discus/step_wise")

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

###### plot all runs #######
library(ggplot2)
p <- ggplot(meltposNum, aes(variable, value, group=factor(runid))) +
  geom_line() +
  theme(legend.position = "none")
p

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
  ggtitle("Experiment: CMO and Discussion on a Sun Graph") +
  expand_limits(x = 55, y = 100)
p







