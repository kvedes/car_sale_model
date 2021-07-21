#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
import os
import tqdm
import numpy as np
import pandas as pd
from selenium import webdriver
from urllib.parse import urlencode, urlparse, ParseResult, urljoin
from posixpath import join
from bs4 import BeautifulSoup
import datetime
from selenium.webdriver.firefox.options import Options
import traceback

@dataclass
class URL:
    brand: str
    model: str
    url: str = "https://www.bilbasen.dk/brugt/bil/" 
    priceto: str = "10000000"
    newandused: str = "usedonly"

    @staticmethod
    def parse_url(url) -> ParseResult:
        return urlparse(url)

    def build_base_url(self) -> str:
        url_parsed = URL.parse_url(self.url)
        path = join(url_parsed.path, self.brand, self.model)
        return urljoin(self.url, path)

    def get_page(self, page_number: int) -> str:
        
        base_url = self.build_base_url()
        url_parsed = URL.parse_url(base_url)

        encoded_query = urlencode(
            {
                "priceto": self.priceto,
                "page": page_number
            }
        )
        url_parsed = url_parsed._replace(query=encoded_query)

        return url_parsed.geturl()


def parse_url(url, driver):
    driver.get(url)

    data = driver.page_source
    soup = BeautifulSoup(data, 'html.parser')
    return soup


def parse_soup(soup):
    results = []

    # Loop over the cars in the page
    for div in soup.select("div[class*=bb-listing-clickable]"):
        headline    = None
        #description = None
        odometer    = None
        year        = None
        price       = None
        horsepower  = None

        # Price
        price = float(div.find(attrs={'class': 'col-xs-3 listing-price'}).text.strip().split()[0].replace('.', ''))

        # Headline
        headline  = div.find(attrs={'class': 'listing-heading darkLink'}).text.strip()

        # Horsepower
        horsepower = float(div.find("span", class_="variableDataColumn").attrs['data-hk'].strip().split()[0])

        # Description
        #description = div.find(attrs={'class': 'listing-description expandable-box'}).text.strip()

        # Region
        region = div.find(attrs={'class': 'col-xs-2 listing-region'}).text.strip()

        # Year and odometer
        datas = div.find_all("div", class_=lambda v: v and 'col-xs-2 listing-data' in v)
        for data in datas:
            data_string = data.text.strip()
            if '.' in data_string:
                odometer = float(data_string.replace('.', ''))
            else:
                if data_string != '-':
                    year = int(data_string.strip())

        results.append((headline, year, odometer, price, horsepower, region))
    return results

def get_number_of_pages(soup):
    
    last_page_number_li = soup.find(
        "div",
        attrs={
            "class": "pager-container"
        }
    ).findAll(
        "li",
        attrs={
            "class":
            "active"
        }
    )

    assert len(last_page_number_li) == 1, \
        f"Got multiple elements for last page {last_page_number_li}"
    
    last_page_number = int(last_page_number_li[0].text)

    return last_page_number

def driver(brand, model, timestamp, output_dir):
    # Configure webdriver
    options = Options()
    options.add_argument("--headless")
    web_driver = webdriver.Firefox(firefox_options=options)
    
    # Get number of pages
    url_obj = URL(brand, model)
    soup = parse_url(url_obj.get_page(1000000), web_driver)
    
    n_pages = get_number_of_pages(soup)
    
    results = []
    for page in tqdm.tqdm(range(1, n_pages)):
        
        cur_url = url_obj.get_page(page)
        try:
            soup = parse_url(cur_url, web_driver)

            results.extend(parse_soup(soup))
        except Exception as e:
            traceback.print_exc()
            print(f"Failed to download page {page}")
    
    web_driver.close()
    
    # Create the dataframe
    df = pd.DataFrame.from_records(
        results,
        columns=[
            'headline',
            'year',
            'odometer',
            'price',
            'horsepower',
            'region'
        ]
    )
    
    # EngineSize
    df['engineSize'] = df.iloc[:, 0].str.extract('(\d,\d)', expand=False)

    print(df.head())
    print(f'Number of cars: {df.shape[0]}')

    # Make sure output dir exists
    os.makedirs(output_dir, exist_ok=True)
    file_name = f'data_{brand}_{model}_{timestamp}.parquet'
    output_path = os.path.join(output_dir, file_name)
    print(f"Writing data to {output_path}")
    
    # Save the file
    df.to_parquet(output_path)

