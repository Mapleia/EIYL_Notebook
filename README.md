# Ecology In Your Life - BIOL 230
Author: Kaede Ito

Winter 2021

# Setup
## Recommended: Anaconda
1. [Install Anaconda](https://docs.anaconda.com/anaconda/install/index.html), a Python environment manager.
2. [Setup](https://docs.anaconda.com/anaconda/navigator/tutorials/r-lang/) a [R](https://www.r-project.org/) environment with conda.

    a) Follow the R Notebook tutorial up until it tells you to create a notebook in the browser.

    b) With the browser UI, navigate to where this notebook is located.
3. Install r packages through Anaconda.

    a) Open your commandline (Anaconda installation comes with one).

    b) Activate your notebook env.
    ```
    conda activate name_of_your_env_you_created
    ```

    c) Install the following R packages.

    ```
    conda install -c r r-tidyverse
    conda install -c r r-lubridate
    conda install -c r r-ggplot2
    conda install -c r r-plotly
    ```
4. Edit the notebook in the browser as you please!

## Docker container
Coming soon!