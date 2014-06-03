PolyProjects
============

A website to link Cal Poly Entrepreneurs and Leaders to Artists, Developers, Engineers, etc.

Get it working
==============

1. Clone Project
2. Add secret.py file in PolyProjects/ with SECRET_KEY
3. Add secret.py file in listings/ with SMTP_EMAIL AND SMTP_PASSWORD
4. Run syncdb
5. Run init.py (Initializes fixtures)
6. Run loaddata on each fixture (skills, categories, majors)
