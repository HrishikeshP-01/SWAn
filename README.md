**S**tatic **W**ebsite **An**alyzer
## What it does
SWAn is a desktop application that lets you analyze the security of static websites. It comes with 3 tools:
### Web Crawler
- Detect all the links (both hidden & visible) in a website
- Reveals vital info about the dependencies of the website
- Reveals the packages the website uses whose known vulnerabilities can be exploited by potential hackers
- Reveals files which might contain vital info
 
![Crawler Result](/images/crawler_result.png)
### XSS Vulnerability Scanner
- Detects basic XSS vulnerabilities that are often found in static website forms
- Analyzes forms of the website as they are the ones targeted by hackers most of the time
- Provides vulnerable form details

![XSS Vulnerability Result](/images/xss_result.png)
### SQL Injection Vulnerability Scanner
- Detects forms that are vulnerable to SQL injection

![SQL Injection Result](/images/sql_result.png)
