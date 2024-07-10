# load in any libraries and modules we need
library(jsonlite)
source("./hartmann6.R")

trial_dir <- commandArgs(trailingOnly=TRUE)[1]
data <- read_json(path=file.path(trial_dir, "parameters.json"))
res <- hartmann6(unlist(data))
Sys.sleep(300)
write(toJSON(list(Hartmann6=res)), file.path(trial_dir, "output.json"))
