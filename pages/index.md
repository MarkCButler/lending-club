# Analysis and machine learning: LendingClub

This site summarizes and provides links to a series of Jupyter notebooks that have been
converted to HTML.

Links to converted jupyter notebooks are labelled with the :simple-jupyter: icon.

## Exploratory Data Analysis

The LendingClub [dataset](https://www.kaggle.com/datasets/wordsforthewise/lending-club)
includes data on accepted and rejected loans from 2007 through 2018 Q2.

<!--
    In this document, relative links to html files such as
        html/1-database-creation.html
    point to Jupyter notebooks that have been converted to html.  The html directory
    containing these converted notebooks is ignored by git in the main branch (due
    to the .gitignore file).  However, this directory is not ignored by the static
    site generator mkdocs-material.  The site published to branch gh-pages therefore
    includes the html directory.

    Note that the command to publish the repo's site is
        poetry run mkdocs gh-deploy --no-history --strict
-->

### [:simple-jupyter: Define data types and create the database](html/1-database-creation.html)

- After preliminary exploration of the data, define a data type for each feature.
- Convert / reformat some columns to facilitate model development.
- Create a SQLite database.

### Data Exploration
