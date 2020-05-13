from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import urllib, json
import re
import requests
import pays


countries_list = ['GAB','ZAF','CMR','MAR','FRA','CHN','USA']


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def get_json_data(url):

    # getting json data from a script on a chinese website

    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    txt_data = html.select('body > script')[0].get_text(strip=True)
    txt_data=txt_data[txt_data.find('['):txt_data.find(']')+1]
    return(json.loads(txt_data))


def print_data_in_js(url):


    var=""
    json_data= get_json_data(url)
    for url in json_data:
        if url["countryShortCode"] in countries_list:
            currentConfirmedCount = url["currentConfirmedCount"]
            confirmedCount = url["confirmedCount"]
            deadCount = url["deadCount"]
            curedCount = url["curedCount"]
            # low_countryShortCode=
            var +="var "+url["countryShortCode"].lower()+"_currentConfirmedCount="+str(currentConfirmedCount)+"; var "+url["countryShortCode"].lower()+"_confirmedCount="+str(confirmedCount)+"; var "+url["countryShortCode"].lower()+"_deadCount="+str(deadCount)+"; var "+url["countryShortCode"].lower()+"_curedCount="+str(curedCount)+";"
    
    f = open("/Users/knectt/Documents/SCHONECT/Engeneering/Projects/Covid19.ga/INT/gabon_json.js", "w")
    f.write(var)
    f.close()
    print("done")



print_data_in_js('http://ncov.dxy.cn/ncovh5/view/en_pneumonia_area?aid=GAB')









