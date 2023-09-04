# Analysis and machine learning: LendingClub

The work is presented in a series of Jupyter notebooks that have been converted to HTML.
Links to these notebooks are labelled below with the Jupyter icon :simple-jupyter:.

## Exploratory Data Analysis

The LendingClub [dataset](https://www.kaggle.com/datasets/wordsforthewise/lending-club)
includes data on accepted and rejected loans from 2007 through 2018 Q2.

<!--
    In this document, relative links to html files such as
        html/1-initial-data-cleaning.html
    point to Jupyter notebooks that have been converted to html.  The html directory
    containing these converted notebooks is ignored by git in the main branch (due
    to the .gitignore file).  However, this directory is not ignored by the static
    site generator mkdocs-material.  The site published to branch gh-pages therefore
    includes the html directory.

    Note that the command to publish the repo's site is
        poetry run mkdocs gh-deploy --no-history --strict
-->

### [:simple-jupyter: Define data types, reformat data, and create the database](html/1-initial-data-cleaning.html)

- After preliminary exploration of the data, define a data type for each feature.
- Convert / reformat some columns to facilitate model development.
- Create a SQLite database.

### :simple-jupyter: Explore features
