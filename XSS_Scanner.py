import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

# these type of vulnerabilities are exploited in user inputs & forms
# get all the forms from html content
def get_all_forms(url):
    soup = bs(requests.get(url).content,"html.parser")
    return soup.find_all("form")

# extract every form detail & attributes
def get_form_details(form):
    details = {}
    # get the form action
    action = form.attrs.get("action").lower()
    # get the form method (POST,GGET,etc.)
    method = form.attrs.get("method","get").lower()
    # get all input details (type, name, etc.)
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type","text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    # puts everything in resulting dictionary
    details["action"]=action
    details["method"]=method
    details["inputs"]=inputs
    return details

# function to submit any given form
def submit_form(form_details,url,value):
    # construct the full url (url provided by action is relative)
    target_url = urljoin(url,form_details["action"])
    # get the inputs
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        # replace all text & search values with 'value'
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            # if input name & value are not None
            # then add them to the data of form submission
            data[input_name] = input_value
        if form_details["method"]=="post":
            return request.post(target_url,datat=data)
        else:
            # GET request
            return requests.get(target_url,params=data)

# function to print all XSS vulnerable forms
# injects JS code in all input fields & submits the form
# if js code is injected & successfully executed then page is XSS vulnerable 
def scan_xss(url):
    form_details=[]
    # get all forms from URL
    forms = get_all_forms(url)
    print(f"[+]Detected {len(forms)} forms on {url}")
    js_script = "<Script>alert('hi')</script>"
    # returning value
    is_vulnerable = False
    # iterate over all forms
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            print("f[+] XSS Detected on {url}")
            print("f[*] Form Details:")
            print(form_details)
            is_vulnerable = True
    return [is_vulnerable, form_details]

if __name__ == "__main__":
    url="https://xss-game.appspot.com/level1/frame"
    print(scan_xss(url)[0])
    
