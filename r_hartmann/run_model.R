# load in any libraries and modules we need
library(jsonlite)
source("./hartmann6.R")

trial_dir <- commandArgs(trailingOnly=TRUE)[1]
data <- read_json(path=file.path(trial_dir, "parameters.json"))
X <- c(data$x1, data$x2, data$x3, data$x4, data$x5, data$x6)
res <- hartmann6(X)
write(toJSON(list(Hartmann6=res)), file.path(trial_dir, "output.json"))
