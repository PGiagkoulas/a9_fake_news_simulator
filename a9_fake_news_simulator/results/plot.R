library("tidyverse")

df1 <- read.csv("sim_runs_10.csv")
df2 <- read.csv("sim_runs_11.csv")
df3 <- read.csv("sim_runs_12.csv")
df4 <- read.csv("sim_runs_13.csv")
df5 <- read.csv("sim_runs_14.csv")
df6 <- read.csv("sim_runs_15.csv")
df7 <- read.csv("sim_runs_16.csv")
df8 <- read.csv("sim_runs_17.csv")
df9 <- read.csv("sim_runs_18.csv")

make_plotdf <- function(datadf) {
  return_plotdf <- datadf %>%
    select(timestep, pos, neg, neut) %>%
    gather(key = "variable", value = "value", -timestep)
  return(return_plotdf)
}

make_basicdf <- function(datadf) {
  return_basicdf <- data.frame(timestep = datadf$current.step,
                               pos = datadf$X.positives,
                               neg = datadf$X.negatives,
                               neut = datadf$X.neutrals)
  return(return_basicdf)
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
