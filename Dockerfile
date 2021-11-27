FROM jupyter/r-notebook:latest
WORKDIR /notebook
COPY . .
RUN R -e "install.packages(c('plotly', 'tidyverse', 'lubridate', 'ggplot2'))"
EXPOSE 8888

