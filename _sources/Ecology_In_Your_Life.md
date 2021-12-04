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

# Overview

+++

**Class:** BIOL 230, W2021

**Written by:** Kaede Ito

+++

## Ecology Question

+++

Given ocean temperatures off the coast of British Columbia, what could be the effect of the 2021 summer Western North America heat wave and how could it have changed the community of algae species (diversity, abundance, new species establishment)?

+++

## Data Sources

+++

For this project, I need data of the ocean surface / close-to-surface temperatures during the summer heatwave period (mid June to late July) and perferably also it's coordinates. This would mean I'd need:
- ocean temperatures (close to the surface)
- time and date in the right range 
- coordinates 
    
I'd also need some sort of anecdotal / observational / measured information of the algae during that time, or based on the known list of algae that resides off the coast of British Columbia, their tolerable temperature ranges.

+++

### Ocean Temperatures

+++

#### National Centers for Environmental Information
[Underway meteorological, navigational, optical, physical, and time series data collected aboard NOAA Ship Ronald H. Brown in the Coastal Waters of Southeast Alaska and British Columbia, Columbia River estuary - Washington/Oregon and others from 2021-06-13 to 2021-07-26 (NCEI Accession 0240415)](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.nodc:0240415)

All information about ocean temperatures was collected from this dataset. The information needed for this analysis was identified through combing through the [metadata](https://www.nodc.noaa.gov/archive/arc0185/0240415/1.1/data/0-data/RB-0_2021-07-27-133235/DeviceConfiguration_20210613-154208.xml) which can be inspected in the browser. 

The `SBE45-TSG-MSG_20210XXX-XXXXXX.Raw` and `SST-TSG-Temp-Diff-MSG_20210XXX-XXXXXX.Raw` were both found to have external (not inside the ship) temperatures measured at different times, so both file types were parsed for more information. Since those files don't measure the GPS location, another file `Primary-GPS-GGA_XXX-XXXXXX.Raw` were matched using timestamps.

To match the timestamps even if the second values are different and to reduce the amount of information shown on the plots, the temperature values and the GPS values were averaged over a minute, then matched using the minute value.

+++

### Temperature Tolerance of Algae

+++
