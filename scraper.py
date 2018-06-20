# -*- coding: utf-8 -*-

#### IMPORTS 1.0

import os
import re
import json
import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup


#### FUNCTIONS 1.0

def validateFilename(filename):
    filenameregex = '^[a-zA-Z0-9]+_[a-zA-Z0-9]+_[a-zA-Z0-9]+_[0-9][0-9][0-9][0-9]_[0-9QY][0-9]$'
    dateregex = '[0-9][0-9][0-9][0-9]_[0-9QY][0-9]'
    validName = (re.search(filenameregex, filename) != None)
    found = re.search(dateregex, filename)
    if not found:
        return False
    date = found.group(0)
    now = datetime.now()
    year, month = date[:4], date[5:7]
    validYear = (2000 <= int(year) <= now.year)
    if 'Q' in date:
        validMonth = (month in ['Q0', 'Q1', 'Q2', 'Q3', 'Q4'])
    elif 'Y' in date:
        validMonth = (month in ['Y1'])
    else:
        try:
            validMonth = datetime.strptime(date, "%Y_%m") < now
        except:
            return False
    if all([validName, validYear, validMonth]):
        return True


def validateURL(url, requestdata):
    try:
        r = requests.get(url, params=requestdata)
        count = 1
        while r.status_code == 500 and count < 4:
            print ("Attempt {0} - Status code: {1}. Retrying.".format(count, r.status_code))
            count += 1
            r = requests.get(url, params=requestdata)
        sourceFilename = r.headers.get('Content-Disposition')

        if sourceFilename:
            ext = os.path.splitext(sourceFilename)[1].replace('"', '').replace(';', '').replace(' ', '')
        else:
            ext = os.path.splitext(url)[1]
        validURL = r.status_code == 200
        validFiletype = ext.lower() in ['.csv', '.xls', '.xlsx']
        return validURL, validFiletype
    except:
        print ("Error validating URL.")
        return False, False


def validate(filename, file_url, requestdata):
    validFilename = validateFilename(filename)
    validURL, validFiletype = validateURL(file_url, requestdata)
    if not validFilename:
        print filename, "*Error: Invalid filename*"
        print file_url
        return False
    if not validURL:
        print filename, "*Error: Invalid URL*"
        print file_url
        return False
    if not validFiletype:
        print filename, "*Error: Invalid filetype*"
        print file_url
        return False
    return True


def convert_mth_strings ( mth_string ):
    month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
    for k, v in month_numbers.items():
        mth_string = mth_string.replace(k, v)
    return mth_string


#### VARIABLES 1.0

entity_id = "E1932_DBC_gov"
url = "http://webapps.dacorum.gov.uk/spendingdata/spendingdownload.aspx"
errors = 0
data = []
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
year_dic = {'2018':{"valid":"%2FwEdABSE8Qt1KlV1J9KeNPIQtTBPE5bA6PjsYbPvOGJjNwlyAa9S5EB8MvMvEr2bCY19cFmJ7WszDpJU6T1weIR4Ie1xxBSZ60%2FHerXDuuv9taVs1QXOQ9MO7e4yLWykoNwhhxGNPl%2B9JJt5%2FrGRi6uIhxF9pFpM53q34CsSY8OiQWOe69rGvmEnaVCrmt7ClYfqyqXHwLNZx5kDV%2BEZj13QqaspCFmVeQ39T1K%2Fb9iPIPYfU2HtwfH%2Fc9y7GjG%2BtOcSWJ7EU2JFh7Ixy6El%2BG5XPxZ2SAncKJa2uhrJcYJt61rVn1eMEqCqplFVx56mfisa7fF3PAMvcIeAZxY%2FKu%2Fu9kT0YoThdbZr%2B2CTJLc00jsYikxTT0xjzFpB7dY1OC5GpNT53d8HLcsMPPSWw23i74K4VDN27krvfpm%2B1IzZ4LdVW4aAZpU%2BpFFMPBtJ49kNKFEDXJelKNaub9Od9FVL%2FM4W", "state":"%2FwEPDwUJODMzNTE1NDU0D2QWAmYPZBYCAgMPZBYEAgkPFgIeBFRleHQFHzxoMT5TcGVuZGluZyBEYXRhIERvd25sb2FkPC9oMT5kAg4PZBYCAhEPD2QPEBYBZhYBFgIeDlBhcmFtZXRlclZhbHVlBQQyMDE4FgFmZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDGN0bDAwJHNlYXJjaHObYZajbV0Qqcyx81vTtkJoyVi1ksSL99cql7PLu055"},
            '2017':{"valid": "%2FwEdABtnlVX4p2%2FeGG%2FBk%2FEpzCPNE5bA6PjsYbPvOGJjNwlyAa9S5EB8MvMvEr2bCY19cFmJ7WszDpJU6T1weIR4Ie1xxBSZ60%2FHerXDuuv9taVs1QXOQ9MO7e4yLWykoNwhhxGNPl%2B9JJt5%2FrGRi6uIhxF9pFpM53q34CsSY8OiQWOe69rGvmEnaVCrmt7ClYfqyqXHwLNZx5kDV%2BEZj13QqaspCFmVeQ39T1K%2Fb9iPIPYfU2HtwfH%2Fc9y7GjG%2BtOcSWJ7EU2JFh7Ixy6El%2BG5XPxZ2SAncKJa2uhrJcYJt61rVn1eMEqCqplFVx56mfisa7fF3PAMvcIeAZxY%2FKu%2Fu9kT0YoThdbZr%2B2CTJLc00jsYikxTT0xjzFpB7dY1OC5GpNRJ%2B7R00ez4JKanodeClR32CIbeuunBml1Q0tx3733lvDmQX8UjihxKztmYmU%2FKDsNwgBghZwAWAIHnn6u%2FHfqXL0%2BkWkQaS83mdW4Xqd7SPZXhbjDQNwkl%2FjO7SMWeursHdfyFhq4xwx0bswivNszN%2Bd3fBy3LDDz0lsNt4u%2BCuFQzdu5K736ZvtSM2eC3VVvL7TedW2T%2BbjuwigJBdGW6cFe5149fu5hFHShNbSBe2A%3D%3D", "state":"%2FwEPDwUJODMzNTE1NDU0D2QWAmYPZBYCAgMPZBYEAgkPFgIeBFRleHQFHzxoMT5TcGVuZGluZyBEYXRhIERvd25sb2FkPC9oMT5kAg4PZBYCAhEPD2QPEBYBZhYBFgIeDlBhcmFtZXRlclZhbHVlBQQyMDE2FgFmZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDGN0bDAwJHNlYXJjaC47UVGwiDjYbQkn9lBWy0zIQ9i%2Bm0r86kfpFkvmSU5U"},
            '2016':{"valid":"%2FwEdABtnlVX4p2%2FeGG%2FBk%2FEpzCPNE5bA6PjsYbPvOGJjNwlyAa9S5EB8MvMvEr2bCY19cFmJ7WszDpJU6T1weIR4Ie1xxBSZ60%2FHerXDuuv9taVs1QXOQ9MO7e4yLWykoNwhhxGNPl%2B9JJt5%2FrGRi6uIhxF9pFpM53q34CsSY8OiQWOe69rGvmEnaVCrmt7ClYfqyqXHwLNZx5kDV%2BEZj13QqaspCFmVeQ39T1K%2Fb9iPIPYfU2HtwfH%2Fc9y7GjG%2BtOcSWJ7EU2JFh7Ixy6El%2BG5XPxZ2SAncKJa2uhrJcYJt61rVn1eMEqCqplFVx56mfisa7fF3PAMvcIeAZxY%2FKu%2Fu9kT0YoThdbZr%2B2CTJLc00jsYikxTT0xjzFpB7dY1OC5GpNRJ%2B7R00ez4JKanodeClR32CIbeuunBml1Q0tx3733lvDmQX8UjihxKztmYmU%2FKDsNwgBghZwAWAIHnn6u%2FHfqXL0%2BkWkQaS83mdW4Xqd7SPZXhbjDQNwkl%2FjO7SMWeursHdfyFhq4xwx0bswivNszN%2Bd3fBy3LDDz0lsNt4u%2BCuFQzdu5K736ZvtSM2eC3VVvL7TedW2T%2BbjuwigJBdGW6cFe5149fu5hFHShNbSBe2A%3D%3D","state":"%2FwEPDwUJODMzNTE1NDU0D2QWAmYPZBYCAgMPZBYEAgkPFgIeBFRleHQFHzxoMT5TcGVuZGluZyBEYXRhIERvd25sb2FkPC9oMT5kAg4PZBYCAhEPD2QPEBYBZhYBFgIeDlBhcmFtZXRlclZhbHVlBQQyMDE2FgFmZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDGN0bDAwJHNlYXJjaC47UVGwiDjYbQkn9lBWy0zIQ9i%2Bm0r86kfpFkvmSU5U"},
            '2015':{"valid":"%2FwEdABvh3jfypoqVq%2FhjFAx49uQtE5bA6PjsYbPvOGJjNwlyAa9S5EB8MvMvEr2bCY19cFmJ7WszDpJU6T1weIR4Ie1xxBSZ60%2FHerXDuuv9taVs1QXOQ9MO7e4yLWykoNwhhxGNPl%2B9JJt5%2FrGRi6uIhxF9pFpM53q34CsSY8OiQWOe69rGvmEnaVCrmt7ClYfqyqXHwLNZx5kDV%2BEZj13QqaspCFmVeQ39T1K%2Fb9iPIPYfU2HtwfH%2Fc9y7GjG%2BtOcSWJ7EU2JFh7Ixy6El%2BG5XPxZ2SAncKJa2uhrJcYJt61rVn1eMEqCqplFVx56mfisa7fF3PAMvcIeAZxY%2FKu%2Fu9kT0YoThdbZr%2B2CTJLc00jsYikxTT0xjzFpB7dY1OC5GpNRJ%2B7R00ez4JKanodeClR32CIbeuunBml1Q0tx3733lvDmQX8UjihxKztmYmU%2FKDsNwgBghZwAWAIHnn6u%2FHfqXL0%2BkWkQaS83mdW4Xqd7SPZXhbjDQNwkl%2FjO7SMWeursHdfyFhq4xwx0bswivNszN%2Bd3fBy3LDDz0lsNt4u%2BCuFQzdu5K736ZvtSM2eC3VVtgxNka8Zl%2BSn4ozbabRVDCAL79U8jbqK9QjofmztK2Sw%3D%3D","state":"%2FwEPDwUJODMzNTE1NDU0D2QWAmYPZBYCAgMPZBYEAgkPFgIeBFRleHQFHzxoMT5TcGVuZGluZyBEYXRhIERvd25sb2FkPC9oMT5kAg4PZBYCAhEPD2QPEBYBZhYBFgIeDlBhcmFtZXRlclZhbHVlBQQyMDE1FgFmZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDGN0bDAwJHNlYXJjaGrtYmL7qxo%2Ffzw%2BDv6vtDC0zSj0q1cPvlIoSwQOAKNv"},
            '2014':{"valid":"%2FwEdABtiS4XMQKH2io4Gup0gZnofE5bA6PjsYbPvOGJjNwlyAa9S5EB8MvMvEr2bCY19cFmJ7WszDpJU6T1weIR4Ie1xxBSZ60%2FHerXDuuv9taVs1QXOQ9MO7e4yLWykoNwhhxGNPl%2B9JJt5%2FrGRi6uIhxF9pFpM53q34CsSY8OiQWOe69rGvmEnaVCrmt7ClYfqyqXHwLNZx5kDV%2BEZj13QqaspCFmVeQ39T1K%2Fb9iPIPYfU2HtwfH%2Fc9y7GjG%2BtOcSWJ7EU2JFh7Ixy6El%2BG5XPxZ2SAncKJa2uhrJcYJt61rVn1eMEqCqplFVx56mfisa7fF3PAMvcIeAZxY%2FKu%2Fu9kT0YoThdbZr%2B2CTJLc00jsYikxTT0xjzFpB7dY1OC5GpNRJ%2B7R00ez4JKanodeClR32CIbeuunBml1Q0tx3733lvDmQX8UjihxKztmYmU%2FKDsNwgBghZwAWAIHnn6u%2FHfqXL0%2BkWkQaS83mdW4Xqd7SPZXhbjDQNwkl%2FjO7SMWeursHdfyFhq4xwx0bswivNszN%2Bd3fBy3LDDz0lsNt4u%2BCuFQzdu5K736ZvtSM2eC3VVt3HgcbU28wNzdhOq396xApmIQ8o2wCEBMs%2FughwIW4zQ%3D%3D","state":"%2FwEPDwUJODMzNTE1NDU0D2QWAmYPZBYCAgMPZBYEAgkPFgIeBFRleHQFHzxoMT5TcGVuZGluZyBEYXRhIERvd25sb2FkPC9oMT5kAg4PZBYCAhEPD2QPEBYBZhYBFgIeDlBhcmFtZXRlclZhbHVlBQQyMDE0FgFmZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDGN0bDAwJHNlYXJjaO2IZM5AtwTBarCAn%2B0egsy%2BINEZVVLjY%2FnK8Izl2QU9"},
            '2013':{"valid":"%2FwEdABumfXN4ROuHGAOjuz%2BUkbsYE5bA6PjsYbPvOGJjNwlyAa9S5EB8MvMvEr2bCY19cFmJ7WszDpJU6T1weIR4Ie1xxBSZ60%2FHerXDuuv9taVs1QXOQ9MO7e4yLWykoNwhhxGNPl%2B9JJt5%2FrGRi6uIhxF9pFpM53q34CsSY8OiQWOe69rGvmEnaVCrmt7ClYfqyqXHwLNZx5kDV%2BEZj13QqaspCFmVeQ39T1K%2Fb9iPIPYfU2HtwfH%2Fc9y7GjG%2BtOcSWJ7EU2JFh7Ixy6El%2BG5XPxZ2SAncKJa2uhrJcYJt61rVn1eMEqCqplFVx56mfisa7fF3PAMvcIeAZxY%2FKu%2Fu9kT0YoThdbZr%2B2CTJLc00jsYikxTT0xjzFpB7dY1OC5GpNRJ%2B7R00ez4JKanodeClR32CIbeuunBml1Q0tx3733lvDmQX8UjihxKztmYmU%2FKDsNwgBghZwAWAIHnn6u%2FHfqXL0%2BkWkQaS83mdW4Xqd7SPZXhbjDQNwkl%2FjO7SMWeursHdfyFhq4xwx0bswivNszN%2Bd3fBy3LDDz0lsNt4u%2BCuFQzdu5K736ZvtSM2eC3VVscx5HtgQG1N%2BfENq39F6MXB9QnCL1H7ZIChFQcPYZVTA%3D%3D","state":"%2FwEPDwUJODMzNTE1NDU0D2QWAmYPZBYCAgMPZBYEAgkPFgIeBFRleHQFHzxoMT5TcGVuZGluZyBEYXRhIERvd25sb2FkPC9oMT5kAg4PZBYCAhEPD2QPEBYBZhYBFgIeDlBhcmFtZXRlclZhbHVlBQQyMDEzFgFmZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDGN0bDAwJHNlYXJjaJ%2F5sNrlgKHz0ybEy6LR1XzLnhVsqRSmUZebIo34YOrH"},
            '2012':{"valid":"%2FwEdABuT7HjAHemp9ygUJ0rA8duiE5bA6PjsYbPvOGJjNwlyAa9S5EB8MvMvEr2bCY19cFmJ7WszDpJU6T1weIR4Ie1xxBSZ60%2FHerXDuuv9taVs1QXOQ9MO7e4yLWykoNwhhxGNPl%2B9JJt5%2FrGRi6uIhxF9pFpM53q34CsSY8OiQWOe69rGvmEnaVCrmt7ClYfqyqXHwLNZx5kDV%2BEZj13QqaspCFmVeQ39T1K%2Fb9iPIPYfU2HtwfH%2Fc9y7GjG%2BtOcSWJ7EU2JFh7Ixy6El%2BG5XPxZ2SAncKJa2uhrJcYJt61rVn1eMEqCqplFVx56mfisa7fF3PAMvcIeAZxY%2FKu%2Fu9kT0YoThdbZr%2B2CTJLc00jsYikxTT0xjzFpB7dY1OC5GpNRJ%2B7R00ez4JKanodeClR32CIbeuunBml1Q0tx3733lvDmQX8UjihxKztmYmU%2FKDsNwgBghZwAWAIHnn6u%2FHfqXL0%2BkWkQaS83mdW4Xqd7SPZXhbjDQNwkl%2FjO7SMWeursHdfyFhq4xwx0bswivNszN%2Bd3fBy3LDDz0lsNt4u%2BCuFQzdu5K736ZvtSM2eC3VVvaAYcI%2B0usNvIdr6CAYJ8rcc98ilKcSANXjIY3q38JrQ%3D%3D","state":"%2FwEPDwUJODMzNTE1NDU0D2QWAmYPZBYCAgMPZBYEAgkPFgIeBFRleHQFHzxoMT5TcGVuZGluZyBEYXRhIERvd25sb2FkPC9oMT5kAg4PZBYCAhEPD2QPEBYBZhYBFgIeDlBhcmFtZXRlclZhbHVlBQQyMDEyFgFmZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDGN0bDAwJHNlYXJjaE9LCarSM8TfqpVC77d8pN84AaCWKyZSSDzivPltuqGk"},
            '2011':{"valid":"%2FwEdABtlKV%2BYSw6B3mQ7SPthvfT6E5bA6PjsYbPvOGJjNwlyAa9S5EB8MvMvEr2bCY19cFmJ7WszDpJU6T1weIR4Ie1xxBSZ60%2FHerXDuuv9taVs1QXOQ9MO7e4yLWykoNwhhxGNPl%2B9JJt5%2FrGRi6uIhxF9pFpM53q34CsSY8OiQWOe69rGvmEnaVCrmt7ClYfqyqXHwLNZx5kDV%2BEZj13QqaspCFmVeQ39T1K%2Fb9iPIPYfU2HtwfH%2Fc9y7GjG%2BtOcSWJ7EU2JFh7Ixy6El%2BG5XPxZ2SAncKJa2uhrJcYJt61rVn1eMEqCqplFVx56mfisa7fF3PAMvcIeAZxY%2FKu%2Fu9kT0YoThdbZr%2B2CTJLc00jsYikxTT0xjzFpB7dY1OC5GpNRJ%2B7R00ez4JKanodeClR32CIbeuunBml1Q0tx3733lvDmQX8UjihxKztmYmU%2FKDsNwgBghZwAWAIHnn6u%2FHfqXL0%2BkWkQaS83mdW4Xqd7SPZXhbjDQNwkl%2FjO7SMWeursHdfyFhq4xwx0bswivNszN%2Bd3fBy3LDDz0lsNt4u%2BCuFQzdu5K736ZvtSM2eC3VVtVmw7wehnuag1yOc8r6ZPHnxbs3HnuPhYP0pnK9ekt1Q%3D%3D","state":"%2FwEPDwUJODMzNTE1NDU0D2QWAmYPZBYCAgMPZBYEAgkPFgIeBFRleHQFHzxoMT5TcGVuZGluZyBEYXRhIERvd25sb2FkPC9oMT5kAg4PZBYCAhEPD2QPEBYBZhYBFgIeDlBhcmFtZXRlclZhbHVlBQQyMDExFgFmZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDGN0bDAwJHNlYXJjaF62uz4npyC0eg0BshNwTSlcUI3N6Hh3pYB8Tf%2FrEwBo"},
            '2010':{"valid":"%2FwEdABBXp3PtT06%2BBCP7zkykpPI%2FE5bA6PjsYbPvOGJjNwlyAa9S5EB8MvMvEr2bCY19cFmJ7WszDpJU6T1weIR4Ie1xxBSZ60%2FHerXDuuv9taVs1QXOQ9MO7e4yLWykoNwhhxGNPl%2B9JJt5%2FrGRi6uIhxF9pFpM53q34CsSY8OiQWOe69rGvmEnaVCrmt7ClYfqyqXHwLNZx5kDV%2BEZj13QqaspCFmVeQ39T1K%2Fb9iPIPYfU2HtwfH%2Fc9y7GjG%2BtOcSWJ7EU2JFh7Ixy6El%2BG5XPxZ2B3X8hYauMcMdG7MIrzbMzfnd3wctyww89JbDbeLvgrhUM3buSu9%2Bmb7UjNngt1VbcBx%2FbMYL%2BEYnnVuyG19KuX%2BqEm2J9dr7Ie2PQyyQOn8%3D","state":"%2FwEPDwUJODMzNTE1NDU0D2QWAmYPZBYCAgMPZBYEAgkPFgIeBFRleHQFHzxoMT5TcGVuZGluZyBEYXRhIERvd25sb2FkPC9oMT5kAg4PZBYCAhEPD2QPEBYBZhYBFgIeDlBhcmFtZXRlclZhbHVlBQQyMDEwFgFmZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDGN0bDAwJHNlYXJjaLesOIWM6gDniRWWOs7aXibENAwRCEi3522uQ%2FBsIXEU"}
            }
#### READ HTML 1.0
import requests

html = requests.get(url)
soup = BeautifulSoup(html.text, 'lxml')

#### SCRAPE DATA

d = """__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE={}&__VIEWSTATEGENERATOR=7D80A3C7&__EVENTVALIDATION={}&ctl00%24searchBox=&ctl00%24MainContent%24ddYYYY={}&ctl00%24MainContent%24ddMMM={}&ctl00%24MainContent%24Button1=&ctl00%24FileCounter=0"""
for k, v in year_dic.items():
    for month in months:
        val = v['valid']
        s = v['state']
        csvMth = month
        csvYr = k
        dat = d.format(s, val, k, month)
        html = requests.get(url, params=dat)
        if html.status_code == 200:
            data.append([csvYr, csvMth, url, dat])


#### STORE DATA 1.0

for row in data:
    csvYr, csvMth, url, requestdata = row
    filename = entity_id + "_" + csvYr + "_" + csvMth
    todays_date = str(datetime.now())
    file_url = url.strip()

    valid = validate(filename, file_url, requestdata)

    if valid == True:
        scraperwiki.sqlite.save(unique_keys=['l'], data={"l": file_url, "f": filename, "d": todays_date })
        print filename
    else:
        errors += 1

if errors > 0:
    raise Exception("%d errors occurred during scrape." % errors)


#### EOF
