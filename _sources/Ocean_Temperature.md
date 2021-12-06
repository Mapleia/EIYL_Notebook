---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: R
  language: R
  name: ir
---

# Ocean Temperature Data Exploring

+++

## Setup

+++

Analysis and visualization was done using R and various packages. The following is the script used to generate 2 scatterplot graphs.

```{code-cell} r
library(tidyverse)
library(lubridate) 
library(ggplot2)
library(plotly)
options(repr.plot.width=10, repr.plot.height=6)
```

## Reading and Wrangling Data

+++

Temperature data {cite}`Dewees2021` are found in the `"data"` folder, while coordinates (and the time recorded) are in the `"data/nav"` folder.

All of the temperature data was cleaned using a `Python` script, located in the `data_cleaning` folder. No packages were used, and can be used as long as a v3.9 Python is installed (anything above or below is untested) and the scripts are pointed to the right data sources.

- `data/temp_processed_summarized.csv`: mean temp over min
- `data/nav/nav_processed.csv`: mean GPS over min
- `data/nav_temp_joined_processed.csv`: joined mean temp & GPS over min

+++

The dates are all of type `character`, meaning extracting any use without it being a proper `date` type is hard. Therefore, time and date must be formatted.

```{code-cell} r
format_datetime <- function(df) {
  df_new <- df %>%
    # https://www.neonscience.org/resources/learning-hub/tutorials/dc-time-series-subset-dplyr-r
    mutate(date = as.Date(date, format = '%m/%d/%Y')) %>%
    # https://www.tidyverse.org/blog/2021/03/clock-0-1-0/
    mutate(datetime = as.POSIXct(date, "America/Vancouver")) %>%
    mutate(datetime = datetime +hour(time)+ minute(time))
  
  return(df_new)
}
```

The following are all of the functions needed to clean up 1 temperature file. However, we have quite a few files, and trying to clean and instantiate each by hand is cumbersome. Therefore, we will iterate through all of the files and summarize.

```{attention}
Please keep in mind that the following code blocks will take pretty long to run.
```

```{code-cell} r
clean_SBE45_data <- function(x) {
  read <- read_delim(x, delim = ",", 
                     col_names = c("date", 
                                    "time", 
                                    "int_temp", 
                                    "conductivity",
                                    "salinity",
                                    "sound_vel",
                                    "ext_temp"),
                    col_types = cols(
                      date = col_character(),
                      time = col_time(format = ""),
                      int_temp = col_double(),
                      conductivity = col_double(),
                      salinity = col_double(),
                      sound_vel = col_double(),
                      ext_temp = col_double()
                    )) %>%
    select(date, time, ext_temp)
  return(read)
}
```

```{code-cell} r
clean_STT_TSG_data <- function(x) {
  read <- read_delim(x, delim = ",",
                     col_names = c("date",
                                   "time",
                                   "type",
                                   "diff",
                                   "ext_temp",
                                   "int_temp",
                                  "extra")
                    ) %>%
    select(date, time)    
  return(read)
}
```

```{code-cell} r
clean_temp_data <- function(x) {
  # https://stackoverflow.com/questions/10128617/test-if-characters-are-in-a-string
  if(grepl("SBE45-TSG-MSG", x, fixed = TRUE)) {
    return(clean_SBE45_data(x))
  } else {
    return(clean_STT_TSG_data(x))
  }
}
```

This is the data before it is summarized by the minute.

```{code-cell} r
# https://stackoverflow.com/questions/11433432/how-to-import-multiple-csv-files-at-once
all_temperature_loaded <- list.files(path = "data/",
             pattern = "*.Raw",
             full.names = T) %>%
  map_df(~clean_temp_data(.))
```

```{code-cell} r
head(all_temperature_loaded)
summary(all_temperature_loaded)
```

```{code-cell} r
all_temperature_cleaned <- all_temperature_loaded %>%
  filter(!is.na(ext_temp)) %>%
  filter(ext_temp > 2) %>%
  format_datetime()

all_temperature <- group_by(all_temperature_cleaned, datetime) %>%
    summarize(mean_ext = mean(ext_temp, na.rm = TRUE))

write_csv(all_temperature, "data/temp_processed_summarized.csv")
```

```{code-cell} r
head(all_temperature)
summary(all_temperature)
```

All of the navigation files will also be cleaned up and summarized in similar manner to the temperature files.

```{code-cell} r
clean_nav_data <- function(x) {
  read <- read_csv(x, 
                   col_names = c(
                     "date",
                     "time",
                     "type",
                     "time_num",
                     "lat",
                     "lat_NS",
                     "long",
                     "long_WE",
                     "gps_quality",
                     "num_sat_view",
                     "hort_dil",
                     "ant_alt",
                     "ant_alt_unit",
                     "geoidal",
                     "geoidal_unit",
                     "age_diff",
                     "diff_station"
                   )
                  ) %>%
    select(date, time, lat, long)
    return(read)
}
```

Below is the raw ocean navigation data.

```{code-cell} r
all_nav_loaded <- list.files(path = "data/nav/",
                      pattern = "*.Raw",
                      full.names = T) %>%
  map_df(~clean_nav_data(.)) %>%
  format_datetime()
```

```{code-cell} r
summary(all_nav_loaded)
```

Since the latitude and longitude are in the degree minutes format, they must be converted.

```{code-cell} r
all_nav <- all_nav_loaded %>%
    group_by(datetime) %>%
    summarize(mean_lat = mean(lat), mean_long = mean(long)) %>%
    mutate(mean_lat = mean_lat/100, mean_long = mean_long/100) %>%
    mutate(deg_lat_int = trunc(mean_lat, 0),
           deg_long_int = trunc(mean_long, 0)) %>%
    mutate(deg_lat_dec = round((mean_lat - deg_lat_int) * 10000),
           deg_long_dec = round((mean_long - deg_long_int) * 10000)) %>%
    mutate(mean_deg_lat = deg_lat_int + deg_lat_dec/(60 * 100),
          mean_deg_long = deg_long_int + deg_long_dec / (60 * 100)) %>%
    select(-deg_lat_int, -deg_long_int, -deg_lat_dec, -deg_long_dec, -mean_lat, -mean_long)


write_csv(all_nav, "data/nav/nav_processed.csv")
```

```{code-cell} r
head(all_nav)
summary(all_nav)
```

Since we have the date and time (by the minute) of both the temperature and it's coordinates, we can match the two columns.

```{code-cell} r
joined_temp_nav <- inner_join(all_temperature, 
                             all_nav,
                             by = c("datetime" = "datetime"))

write_csv(joined_temp_nav, "data/nav_temp_joined_processed.csv")
```

```{code-cell} r
head(joined_temp_nav)
summary(joined_temp_nav)
```

## Visualizing the Data

+++

Time and mean temperature plotted on a scatterplot to see temperature changes over time. Notice that since the ship moves in 1 way vs time, the shape of the 2D scatterplot and the 3D plot is very similar.

```{code-cell} r
time_plot <- ggplot(all_temperature, aes(x = datetime, 
                                         y = mean_ext, 
                                         colour = mean_ext)) +
  geom_point() +
  scale_colour_gradient(low = "blue", high = "red") +
  labs(x = "Date and Time PST", 
       y = "Mean (min) Ocean Temperature (°C)",
       colour = "Mean Ocean Temperature (°C)")
time_plot
```

```{code-cell} r
p<- plot_ly(joined_temp_nav, 
        x = ~mean_deg_lat, 
        y = ~mean_deg_long,
        z = ~mean_ext,  
        color = ~mean_ext
        ) %>%
    add_markers(size = 0.7) %>% 
    colorbar(title = "Mean Ocean Temp (°C)")%>%
    layout(title = "Mean Ocean Temperature and Coordinates",
           scene = list(
               xaxis = list(title = "Mean Latitude (°)"),
               yaxis = list(title = "Mean Longitude (°)"),
               zaxis = list(title = "Mean Ocean Temp (°C)")
               )
           )
```

```{code-cell} r
embed_notebook(p)
```
