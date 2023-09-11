# load in any libraries and modules we need
library(SWATrunR)
library(here)

# Loading a SWAT+ demo project
path_plus <- load_demo(dataset = 'project',
                       path = here(),
                       version = 'plus')
