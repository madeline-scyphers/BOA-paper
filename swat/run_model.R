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

print(par_comb)

sim <- run_swatplus(
    project_path=project_path,
    start_date = start_date,
    end_date = end_date,
    years_skip = 0,
    run_path=trial_dir,
    keep_folder=TRUE,
    parameter = par_comb,
    output = list(
        flo_out = define_output(
            file = 'reservoir_day',
            # file = 'channel_sd_day',
            variable = 'flo_out',
            unit = 1),
        solp_out = define_output(
            file = 'reservoir_day',
            variable = 'solp_out',
            unit = 1),
        sedp_out = define_output(
            file = 'reservoir_day',
            variable = 'sedp_out',
            unit = 1),
        sed_out = define_output(
            file = 'reservoir_day',
            variable = 'sed_out',
            unit = 1)
            )
        )

obs<-read_csv(here("swat","obs_data.csv"))
obs <- obs %>% filter(between(date, as.Date(start_date), as.Date(end_date)))

flow_obs <- obs %>% filter(variable == "flow_cms") %>% within(rm(variable))
solp_obs <- obs %>% filter(variable == "SRP_kg") %>% within(rm(variable))
sed_obs <- obs %>% filter(variable == "SS_ton") %>% within(rm(variable))
totp_obs <- obs %>% filter(variable == "TP_kg") %>% within(rm(variable)) %>% filter(date %in% solp_obs$date)

flow_sim <- sim$simulation$flo_out %>% filter(date %in% flow_obs$date)
solp_sim <- sim$simulation$solp_out %>% filter(date %in% totp_obs$date)
sedp_sim <- sim$simulation$sedp_out %>% filter(date %in% totp_obs$date)
sed_sim <- sim$simulation$sed_out %>% filter(date %in% sed_obs$date)
totp_sim <- within(sedp_sim, rm(date)) + within(solp_sim, rm(date))

if (!is.null(flow_sim)) {
    jsn <- toJSON(list(
        flo_out=list(
            y_pred=flow_sim$run_1,
            y_true=flow_obs$value
        ),
        totp=list(
            y_pred=totp_sim$run_1,
            y_true=totp_obs$value
        ),
        solp_out=list(
            y_pred=solp_sim$run_1,
            y_true=solp_obs$value
        ),
        sed_out=list(
            y_pred=sed_sim$run_1,
            y_true=sed_obs$value
        )
    ), pretty = FALSE)
    write(jsn, file.path(trial_dir, "output.json"))
} else {
    write(toJSON(list(trial_status=unbox("FAILED"))), file.path(trial_dir, "output.json"))
}
