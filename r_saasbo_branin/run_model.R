# load in any libraries and modules we need
library(jsonlite)

trial_dir <- commandArgs(trailingOnly=TRUE)[1]
data <- read_json(path=file.path(trial_dir, "filtered_parameters.json"))
params <- rep(NA, length(data$branin))
for(i in 1:length(params)) {
    params[i] <-data$branin[i]
}
write(toJSON(list(branin=params), auto_unbox=TRUE), file.path(trial_dir, "output.json"))
