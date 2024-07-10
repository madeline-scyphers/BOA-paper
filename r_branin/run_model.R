library(jsonlite)

trial_dir <- commandArgs(trailingOnly=TRUE)[1]
data <- read_json(path=file.path(trial_dir, "parameters.json"))
write(toJSON(list(branin=data), auto_unbox=TRUE), file.path(trial_dir, "output.json"))
