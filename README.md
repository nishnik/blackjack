Info
===
**Blackjack** is a surgeon bot who adds past year grade distributions of courses on metaKGP. It searches for all the courses on metaKGP and populates their infoboxes with their previous year grade distributions, if available from ERP.


Setup
=====

* Clone from the pywikibot library from wikimedia to  `~/blackjack`
```
git clone https://gerrit.wikimedia.org/r/pywikibot/core.git ~/blackjack
cd ~/blackjack
```
Create a `user-config.py` file with the following data replacing 'blackjack' with the bot's name:
```python
mylang = 'en'
family = 'metakgp'
usernames['metakgp']['en'] = 'blackjack'
```

* Generate user and family files.
```
python generate_user_files.py
```
```
python generate_family_files.py
```
One first needs to add the cookie, i.e. the jsession ID for visiting the `/Acad` route in erp. To obtain the jsession ID:

# Go to `Student Academic Activities (UG)` section in `Academic`. This gives you a cookie for accesing the `/Acad` route. You will not be able to mine the grades without this.

# Go to `https://erp.iitkgp.ernet.in/Acad/Pre_Registration/subject_grade_status.jsp?subno=XXXXXXX` and refresh the page while having the networking tab on Google Chrome's Inspector on. View the headers of the request to see what jsession ID you must input in `blackjack.py`. 

* Mine grades of all courses from `https://erp.iitkgp.ernet.in/Acad/Pre_Registration/subject_grade_status.jsp?subno=XXXXXXX` after signing in and save it to `allCourses.json`

* Run blackjack
```
python blackjack.py
```
