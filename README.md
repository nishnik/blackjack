Info
===
**Blackjack** is a surgeon bot who adds past year grade distributions of courses on metaKGP. It searches for all the courses on metaKGP and populates their infoboxes with their previous year grade distributions, if available from ERP.


Setup
=====

Clone from the pywikibot library from wikimedia to  `blackjack`
```
git clone https://gerrit.wikimedia.org/r/pywikibot/core.git blackjack
cd blackjack
git clone https://github.com/metakgp/blackjack.git
```

Generate family files.
```
python generate_family_file.py https://wiki.metakgp.org/w/Main_Page metakgp
```

One first needs to add the cookie, i.e. the jsession ID for visiting the `/Acad` route in erp. To obtain the jsession ID:

1. Go to `Student Academic Activities (UG)` section in `Academic`. This gives you a cookie for accesing the `/Acad` route. You will not be able to mine the grades without this.

2. Get the content of the `JSID#/Acad` named cookie set by ERP. It should be something like `43E........26F.worker3`. Update this in `getNewGrades.py`. 

After that, one can mine grades of all courses using `python getNewGrades.py` which saves the new grades to `newGrades.json`

Run blackjack
```
python blackjack.py
```
