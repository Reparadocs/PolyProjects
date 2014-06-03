PolyProjects
============

A website to link Cal Poly Entrepreneurs and Leaders to Artists, Developers, Engineers, etc.

Get it working
==============

1. Clone Project
2. Add .env file with SECRET_KEY, SMTP_EMAIL, SMTP_PASSWORD, and ADDED_SECURITY_STRING
3. Do something with heroku databse stuff in settings.py
4. Run syncdb
5. Run init.py (Initializes fixtures)
6. Run loaddata on each fixture (skills, categories, majors)
