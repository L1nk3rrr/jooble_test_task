# POS: JUNIOR STRONG PYTHON DEVELOPER JOOBLE

## Task requirements

What to do:
1. For each URL get additional information:
   - If redirect occurs -> get the final URL
   - Get the status code of the page,
   - Get page Title (parse from html)
   - Get the domain name of the site
   - Remember the date and time when you received additional information
2. Develop an asynchronous web service that implements the API with the following functionality:
    2.1 Getting data from an input file by domain
    - Parameter at the input: 
       - Domain name
    - Response: json with the following information:
      - date and time of first visit
      - date and time of the last visit
      - number of pages visited
      - number of active visited pages (status_code = 200)
      - URL list
     - #### Example
     
    ```json
    Request(post): {"domain_name": "cyberchimps.com"}
    Response: 
   {
	    "last_visit_date": "2021-05-07 04:09:04"
	    "first_visit_date": "2021-01-07 21:01:43",
	    "page_count": 3,
	    "active_page_count": 3,
	    "url_list": [
		    "https://cyberchimps.com/blog/top-wordpress-photography-themes/"
		    "https://cyberchimps.com/blog/best-wordpress-themes-for-artists/"
		    "https://cyberchimps.com/blog/"
	    ]
    }
    ```
    2.2 Get data from the input file of the last visited URL:
Input parameter
    - Parameter at the input: 
       - URL
    - Response: json with the following information:
       - date and time of visit (data from spreadsheet)
       - final URL (if there was a redirect)
       - page status_code
       - page title
       - site domain name
       - date and time when additional information was received
     - #### Example
    ```json
    Request(post): {"domain_name": "https://cyberchimps.com/blog/"}
    Response: 
    {
	    "visit_date": "2021-01-07 21:01:43"
	    "final_url": "",
	    "status_code": 200,
	    "title": "Free & Premium WordPress Themes Blog, WP Themes",
	    "domain_name": "cyberchimps.com"
	    "parse_date": "2022-03-07 16:10:15"
    }
    ```

## Installation

Install the last version of python from official site [Python](https://www.python.org/downloads/) (I used python3.11).

Clone repo to your local machine

```sh
git clone https://github.com/L1nk3rrr/jooble_test_task.git
```

Then open working directory and create virtualenv and install requirements

```sh
# Ubuntu
$ python3 -m venv /path/to/new/virtual/environment
$ source /path/to/new/virtual/environment/bin/activate
$ pip3 install -r requirements.txt
# Windows
PS C:\>python -m venv \path\to\new\virtual\environment
PS C:\>\path\to\new\virtual\environment\Scripts\Activate.ps1.bat
(venv_name) PS C:\>pip install -r requirements.txt
```
## How to run
```sh
# Ubuntu
python3 app.py
# Windows
python app.py
```
## EndPoint
So application have only 1 point ```api/get_visit``` and can be used only with POST method.
As in example, you must to sent "domain_name" attribute in form or json part of request (it fetch one of them, see code), if you attr is missed you will have at reponse status_code = 400.
Endpoint work with urls and domain, it will validate your input to know what it is, after that it will query db, if smth found -> you will recieve data in json attr at your response, else 404 -> nothing founded.
## Example of requests
```
REQUEST: res = requests.post("http://127.0.0.1:5000/api/get_visit",
                             data={"domain_name": "ditulis.id"})
RESPONSE: res.json()
{
    "active_pages":11,
    "first_visit_date":"2021-01-02 09:31:15",
    "last_visit_date":"2021-12-14 22:23:34",
    "page_count":13,
    "url_list":[
        "https://ditulis.id/?s=kerja#google_vignette",
        "https://ditulis.id/9-tips-untuk-mempertimbangkan-tawaran-pekerjaan/",
        "https://ditulis.id/",
        "https://ditulis.id/5-cara-milenial-merevolusi-tempat-kerja/",
        "https://ditulis.id/8-skills-cara-membangun-tim-yang-efektif/",
        "https://ditulis.id/rencana-perbaikan-berkelanjutan-di-tempat-kerja/",
        "https://ditulis.id/12-cara-meningkatkan-fokus-di-tempat-kerja-dengan-mudah/",
        "https://ditulis.id/apa-perbedaan-antara-pekerjaan-dan-karir/",
        "https://ditulis.id/kerja-online-untuk-pelajar-beberapa-tanpa-modal/",
        "https://ditulis.id/contoh-surat-lamaran-kerja-yang-baik-dan-benar/",
        "https://ditulis.id/bagaimana-cara-menumbuhkan-rasa-empati-tempat-kerja/",
        "https://ditulis.id/cara-menulis-surat-lamaran-kerja/",
        "https://ditulis.id/kemampuan-negosiasi-yang-wajib-dikuasai/"
    ]
}
```
```
REQUEST: res = requests.post("http://127.0.0.1:5000/api/get_visit",
                             data={"domain_name": "https://jooble.org/jobs-work-from-home-email-sending"})
RESPONSE: res.json()
{
    "domain_name":"jooble.org",
    "final_url":"",
    "parsed_date":"2022-12-05 04:21:37",
    "status_code":200,
    "title":"Urgent! Work from home email sending jobs - December 2022 (with Salaries!) - Jooble",
    "visit_date":"2021-12-11 21:38:36"
}
```
## Addons
If you want to recreate db delete old one, uncomment part of code lower at app.py, that will create a new db.
```sh
    # with app.app_context():
    #     db.create_all()
```
After that simply run application from previous step.
For importing new data for that db, you need to have ```.xlsx``` file from test task, and configured ```.env``` file such this:
```env
API_USER=YOUR_USER_NAME
API_PASSWORD=YOUR_PASSWORD
```
After that configuration simply run ```import_from_xlxs.py```  and wait, until it parsed all urls from xlsx file and save it via api at service side.