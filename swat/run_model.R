# Run Rscript setup.R first in this directory to create a SWAT+ demo project in the current directory
# (linux tested, does not run on Mac, SWATrunR says it runs with Windows, so probably Windows is ok)

# load in any libraries and modules we need
library(SWATrunR)
library(jsonlite)
library(dplyr)
library(here)
library(readr)

project_path <- here("swat", "TxtInOut")
trial_dir <- commandArgs(trailingOnly=TRUE)[1]
data <- read_json(path=file.path(trial_dir, "parameters.json"))

start_date <- data$start_date
end_date <- data$end_date
data <- within(data, rm(start_date, end_date))

par_comb = c()
for (name in names(data)) {
    par_comb[paste(name, " | change = absval")] = data[[name]]
}

sim <- run_swatplus(
    project_path=project_path,
    start_date = start_date,
    end_date = end_date,
    years_skip = 0,
    run_path=trial_dir,
    keep_folder=TRUE,
    parameter = par_comb,
    output = define_output(
            file = 'channel_sd_day',
            variable = 'flo_out',
            unit = 1)
        )

obs<-read_csv(here("swat","obs_data.csv"))
obs <- obs %>% filter(between(date, as.Date(start_date), as.Date(end_date)))

flow_obs <- obs %>% filter(variable == "flow_cms") %>% within(rm(variable))
flow_sim <- sim$simulation$flo_out %>% filter(date %in% flow_obs$date)

if (!is.null(flow_sim)) {
    jsn <- toJSON(list(
        flo_out=list(
            y_pred=flow_sim$run_1,
            y_true=flow_obs$value
        )
    ), pretty = TRUE)
    write(jsn, file.path(trial_dir, "output.json"))
} else {
    write(toJSON(list(trial_status=unbox("FAILED"))), file.path(trial_dir, "output.json"))
}
