import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint

# initailize an HTTP session & set the browser
s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

def get_all_forms(url):
    soup = bs(s.get(url).content,"html-parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    # get the form action (target url)
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    # get the form method (POST, GET, etc.)
    method = form.attrs.get("method","get").lower()
    # get all the input details such as type & name
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type","text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value","")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

# fn that checks whether a webpage has SQL errors in it
# determines whether a page is SQL Injection vulnerable from its response
def is_vulnerable(response):
    errors = [
        # MySQL
        "you have an error in you sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
        ]
    for error in errors:
        # if one of these errors found return True
        if error in response.content.decode().lower():
            return True
    # no error detected
    return False

# fn to place quotes in input fields of all forms in web page
def scan_sql_injection(url):
    vulnerabilityDetected = False
    form_details = []
    # test on URL
    for c in "\"'":
        # add quote/double quote character to URl
        new_url = f"{url}{c}"
        print("[!] Trying",new_url)
        # make the HTTP request
        res = s.get(new_url)
        if is_vulnerable(res):
            # SQL Injection detected on the URL itself
            # no need to proceed for extracting forms & submitting them
            print("[+] SQL Injection vulnerability detected, link:",new_url)
            vulnerabilityDetected = True
            return [vulnerabilityDetected, form_details]
        # test on html forms
        forms = get_all_forms(url)
        print(f"[+] Detected {len(forms)} forms on {url}")
        for form in forms:
            form_details = get_form_details(form)
            for c in "\"'":
            # the data body we want to submit
                data = {}
                for input_tag in form_details["inputs"]:
                    if input_tag["type"] == "hidden" or input_tag["value"]:
                        # any input form that is hidden or has some value
                        # just use it in the form body
                        try:
                            data[input_tag["name"]] = input_tag["value"]+c
                        except:
                            pass
                    elif input_tag["type"] != "submit":
                        # use junk data with special characters for all others except submit
                        data[input_tag["name"]] = f"test{c}"
                # join the url with the action
                url = urljoin(url,form_details["action"])
                if form_details["method"] == "post":
                    res = s.post(url,data=data)
                elif form_details["method"]=="get":
                    res = s.get(url,params=data)
                # test whether the resulting page is vulnerable
                if is_vulnerable(res):
                    print("[+] SQL Injection vulnerability detected, link:",url)
                    print("[+]Form:")
                    pprint(form_details)
                    return [vulnerabilityDetected, form_details]

if __name__ == "__main__":
    url = "http://testphp.vulnweb.com/artists.php?artist=1"
    scan_sql_injection(url)
