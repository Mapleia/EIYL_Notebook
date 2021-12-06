# Project Info & Setup
See the notebook online [here](https://mapleia.github.io/EIYL_Notebook/README.html)!
## Install and Environment Setup
### Recommended: Anaconda
1. [Install Anaconda](https://docs.anaconda.com/anaconda/install/index.html), a Python environment manager.
2. [Setup](https://docs.anaconda.com/anaconda/navigator/tutorials/r-lang/) a [R](https://www.r-project.org/) environment with conda.

    a) Follow the R Notebook tutorial up until it tells you to create a notebook in the browser (use `v3.7.11 Python` and the latest `R` if you are running the jupyter-notebook on Windows 10.)
    > This is due to an dependency error for Python >=v3.8. Read more about the issue [here](https://github.com/executablebooks/jupyter-book/issues/906).

3. Install R packages through Anaconda.

    a) Open your commandline (Anaconda installation comes with one).

    b) Activate your notebook env.
    ```powershell
    conda activate name_of_your_env_you_created
    ```

    c) Install the following R packages.

    ```powershell
    conda install -c r r-tidyverse
    conda install -c r r-lubridate
    conda install -c r r-ggplot2 # (you might not need to install this one, depending on what is pre-installed for you by Anaconda)
    conda install -c r r-plotly
    conda install -c conda-forge r-cowplot
    ```
4. Edit the notebook in the browser (or your jupyter supported editor/IDE) as you please!


## Importing to Github Pages
### Following [this tutorial](https://jupyterbook.org/publish/gh-pages.html):

Run these steps after every major update to publish the changes.

```
{attention}
With the right conda env activated, make sure that you have an installation of `jupyter-book`.
> **Conda**: `conda install -c conda-forge jupyter-book`.
```
1. In a terminal (with the conda environment activated), move to the notebook directory.
    ```
    cd C:/ABSOLUTE/PATH/TO/PROJECT/ROOT/FOLDER
    ```
2. Run `jupyter-book build .`.
3. Run `ghp-import -n -p -f _build/html` .


