# LinkedIn-Scraper-Telegram-Bot

This repo contains the code for a Telegram-Bot that performs LinkedIn scraping. It was never deployed to Heroku or another
hosting site, but it was working locally when the project was finished. 

### Some helful Tips ...

#### Git

Update the remote git repo with your changes.
```
git add .
git commit -m "your message about commit"
git push
```

Update your local repo with remote changes.
```
git pull
```

Create a new branch and checkout
```
git checkout -b branch_name
```

#### Anaconda

Activate a virtual environment
```
conda activate botEnv
```

Once in the virtual enviromnet, install a package
```
conda install package_name
// OR
pip install package_name
```

Export and import virtual environment to/from .yml file.

```
conda env export --name botEnv > environment.yml
conda env create --file environment.yml
```

### pip

Create requirements.txt
```
pip freeze > requirements.txt
```
### Packages

If you get an error about no license key, you may need to run the code below in order for xlwings to work.
```
conda install -c conda-forge xlwings
```
