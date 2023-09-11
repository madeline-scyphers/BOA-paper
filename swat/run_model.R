# Run Rscript setup.R first in this directory to create a SWAT+ demo project in the current directory
# (linux tested, does not run on Mac, SWATrunR says it runs with Windows, so probably Windows is ok)

# load in any libraries and modules we need
library(SWATrunR)
library(jsonlite)
library(dplyr)
library(here)

project_path <- file.path(here(), "swatplus_rev59_demo")

trial_dir <- commandArgs(trailingOnly=TRUE)[1]
data <- read_json(path=file.path(trial_dir, "parameters.json"))

par_comb <- c('lat_ttime.hru | change = absval' = data$lat_ttime,
              'epco.hru | change = absval' = data$epco,
              'esco.hru | change = absval' = data$esco,
              'alpha.aqu | change = absval' = data$alpha)

sim <- run_swatplus(
    project_path=project_path,
    run_path=trial_dir,
    keep_folder=TRUE,
    parameter = par_comb,
    output = define_output(
        file = 'channel_day',
        variable = 'flo_out',
        unit = 1))

if (!is.null(sim$simulation$flo_out)) {
    flo_out <- sim$simulation$flo_out %>%
               select(run_1) %>%
               summarise('flo_out'=sum(run_1))
    write(toJSON(unbox(flo_out)), file.path(trial_dir, "output.json"))
} else {
    write(toJSON(list(trial_status=unbox("FAILED"))), file.path(trial_dir, "output.json"))
}
