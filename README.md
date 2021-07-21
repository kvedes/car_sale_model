# Scrape bilbasen
This is a fork of `CAR_SALE_MODEL` by tjansson60. The original repo is mostly a collection of scripts, where this fork moves more towards being an application. This is mostly reflected by the fact that the code is wrapped up in a package using poetry. It is possible to pip install it as well.
The main functional change from the original repo is that you can supply car brand and name through the cli and you don't have to modify the script based on the number of pages available on bilbasen for that cat.

## Requirements

Beside all the usual stuff as scikit-learn, pandas, seaborn etc. there are some extra dependencies. Selenium is needed
to scrape the danish car sales website, where I intended to sell my car.

```
$ pip install selenium
```

Download the firefox headleass driver from:
- https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz

```
$ tar -xvzf  geckodriver-v0.23.0-linux64.tar.gz
$ chmod +x geckodriver
$ mv geckodriver ~/bin/
```

If you are using Arch linux you can install the driver from pacman
```
sudo pacman -S geckodriver
```

## Installation
In order to install run the following commands:
```
git clone https://github.com/kvedes/car_sale_model.git
cd car_sale_model
pip install .
```

# How to use
Once the package is installed, the application can be called from the cli using the command `bilbasen`. It takes the following arguments:
* BRAND: The name of the car brand e.g. opel, peugeot, skoda
* MODEL: The model of the car e.g. astra, 508, octavia
* --output-dir: Optional argument which is the path where the output data is stored. If the folder doesnt exist it will be created by the script. Defaults to `~/data`. 

Data is saved to a parquet file which has the brand and model in the name along with a timestamp.

## Examples
Scrape data for Opel Astra
```
bilbasen opel astra
```

Scrape data for a Peugeot 508 saving to the path `~/work/cars`
```
bilbasen peugeot 508 --output-dir ~/work/cars
```
