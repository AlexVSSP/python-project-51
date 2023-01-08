# python-project-51
[![Actions Status](https://github.com/AlexVSSP/python-project-51/workflows/hexlet-check/badge.svg)](https://github.com/AlexVSSP/python-project-51/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/6c23c6d3e11f35e93e61/maintainability)](https://codeclimate.com/github/AlexVSSP/python-project-51/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/6c23c6d3e11f35e93e61/test_coverage)](https://codeclimate.com/github/AlexVSSP/python-project-51/test_coverage)
[![Python CI](https://github.com/AlexVSSP/python-project-50/actions/workflows/pyci.yml/badge.svg)](https://github.com/AlexVSSP/python-project-50/actions/workflows/pyci.yml)

### Requirements
- Python version: ^3.8
- Poetry version: ^1.0.0

### Description of the project:

This utility downloads the page from the network and puts it in the specified existing directory. 
In addition, the full path of the downloaded file is displayed on the screen.

## How to install

- First you need to clone the repository:
```
    git clone git@github.com:AlexVSSP/python-project-51.git
    cd python-project-51
```
- Use commands:
```
    make install
    make build
    make package-install
```

## How to use

- To open the help menu:
```
    page-loader -h
```
- Thus, you need to enter the 'page-loader' command, 
specify the directory where the file will be saved (by default, it's a current working directory), 
and also enter URL of the page. For example:
```  
    page-loader https://page-loader.hexlet.rapl.co/
```
- Please note that utility also downloads all resources from the given page, 
which are located at the same address 


### Download the page
[![asciicast](https://asciinema.org/a/537086.svg)](https://asciinema.org/a/537086)

### Downloading images
[![asciicast](https://asciinema.org/a/540327.svg)](https://asciinema.org/a/540327)

### Downloading all resources
[![asciicast](https://asciinema.org/a/541321.svg)](https://asciinema.org/a/541321)

### Installation the utility and example of work
[![asciicast](https://asciinema.org/a/544505.svg)](https://asciinema.org/a/544505)

### Example with the appearance of an error
[![asciicast](https://asciinema.org/a/544511.svg)](https://asciinema.org/a/544511)

### Installation the utility and example of work with "progress" library
[![asciicast](https://asciinema.org/a/544505.svg)](https://asciinema.org/a/544505)