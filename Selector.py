import XSS_Scanner as xs
import SQL_Scanner as sq
import Crawler2 as cr

def perform_analysis(c,url):
    try:
        if c == "Web Crawler":
            ret_list = cr.PerformCrawl(url)
            return(ret_list)
        elif c == "XSS Vulnerability Scanner":
            res = xs.scan_xss(url)
            if res[0] == True:
                ret_list = [
                    "[+] XSS Detected on {}".format(url),
                    "[+] Form Details:",
                    str(res[1]),
                    "[+] Analysis Result: IS VULNERABLE",
                    ]
            else:
                ret_list = [
                    "[+] XSS not Detected on {}".format(url),
                    "[+] Analysis Result: IS NOT VULNERABLE",
                    ]
            return ret_list
        elif c == "SQL Injection Vulnerability Scanner":
            res = sq.scan_sql_injection(url)
            if res[0] == True:
                ret_list = [
                    "[+] SQL Injection Vulnerability detected on {}".format(url),
                    # "[+] Form Details:",
                    # str(res[1]),
                    "[+] Analysis Result: IS VULNERABLE",
                    ]
            else:
                ret_list = [
                    "[+] SQL Injection Vulnerability not detected on {}".format(url),
                    "[+] Analysis Result: IS NOT VULNERABLE",
                    ]
            return ret_list
    except:
        ret_list = [
            "[+] Analysis Result: IS NOT VULNERABLE",
            ]
        return ret_list
        
    
        
