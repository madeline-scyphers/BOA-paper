# (linux tested, does not run on Mac, SWATrunR says it runs with Windows, so probably Windows is ok)

# load in any libraries and modules we need
library(SWATrunR)
library(jsonlite)
library(dplyr)
library(here)
library(readr)
library(hydroGOF)

project_path <- here("swat", "TxtInOut")
trial_dir <- commandArgs(trailingOnly=TRUE)[1]
data <- read_json(path=file.path(trial_dir, "parameters.json"))

start_date <- data$start_date
end_date <- data$end_date
years_skip <- data$years_skip
data <- within(data, rm(start_date, end_date, years_skip))

par_comb = c()
for (name in names(data)) {
    par_comb[paste(name, " | change = absval")] = data[[name]]
}

sim <- run_swatplus(
    project_path=project_path,
    start_date = start_date,
    end_date = end_date,
    years_skip = years_skip,
    run_path=trial_dir,
    parameter = par_comb,
    output = define_output(
            file = 'channel_sd_day',
            variable = 'flo_out',
            unit = 1)
        )

obs <- read_csv(here("swat","obs_data.csv"))
obs <- obs %>% filter(between(date, min(sim$simulation$flo_out$date), as.Date(end_date)))

flow_obs <- obs %>% filter(variable == "flow_cms") %>% within(rm(variable))
flow_sim <- sim$simulation$flo_out %>% filter(date %in% flow_obs$date)

# NSE (Nash–Sutcliffe model efficiency coefficient)
nse <- NSE(sim=flow_sim$run_1, obs=flow_obs$value)
if (!is.null(nse)) {

    jsn <- toJSON(list(
        flo_out_NSE=nse
    ), pretty = TRUE)
    write(jsn, file.path(trial_dir, "output.json"))
} else {
    write(toJSON(list(trial_status=unbox("FAILED"))), file.path(trial_dir, "output.json"))
}
