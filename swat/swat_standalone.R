# Run Rscript setup.R first in this directory to create a SWAT+ demo project in the current directory
# (linux tested, does not run on Mac, SWATrunR says it runs with Windows, so probably Windows is ok)

# load in any libraries and modules we need
library(SWATrunR)
library(here)
library(jsonlite)

project_path <- here("swat", "TxtInOut")


par_comb <- c(
            #   "erod_fact.channel | change = absval" = 0.00015,
            #   "bed_load.channel | change = absval" = 0,
            #   "surq_lag.basin | change = absval" = 3,
            #   "n_uptake.basin | change = absval" = 20,
              "pperco.bsn | change = absval" = 10,
            #   "p_soil.basin | change = absval" = 150,
              "cn3_swf.hru | change = absval" = 0.1,
              "perco.hru | change = absval" = 0.5,
              "snofall_tmp.hru | change = absval" = 0,
              "snomelt_tmp.hru | change = absval" = 4.5,
              "snomelt_max.hru | change = absval" = 3,
              "snomelt_min.hru | change = absval" = 2

            #   'epco.hru | change = absval' = data$epco,
            #   'esco.hru | change = absval' = data$esco,
            #   'alpha.aqu | change = absval' = data$alpha,
              )

print(project_path)
trial_dir = "/users/PAS0409/madelinescyphers/BOA-paper/swat/swat_plus_demo_20230912T223737/000000"

sim <- run_swatplus(
    project_path=project_path,
    start_date = 20150101,
    end_date = 20150131,
    years_skip = 0,
    run_path=trial_dir,
    keep_folder=TRUE,
    # parameter = par_comb,
    output = define_output(
        file = 'channel_sd_day',
        variable = 'flo_out',
        unit = 1)
        )

# sim <- run_swatplus(
#     project_path=project_path,
#     start_date = 20150101,
#     end_date = 20150131,
#     years_skip = 0,
#     parameter = par_comb,
#     output = define_output(
#         file = 'channel_sd_day',
#         variable = 'flo_out',
#         unit = 1)
#         )

print(sim$simulation$flo_out$run_1)
obs<-read.csv(here("swat","BR_flo.csv"))
jsn <- toJSON(list(
    y_pred=sim$simulation$flo_out$run_1,
    y_true=obs$value))
print(jsn)

write(jsn,
      here("swat", "output.json"))

write.csv(sim$simulation$flo_out, here("swat", "output.csv"))
