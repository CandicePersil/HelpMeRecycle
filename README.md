# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Help_Me_Recycle version control

### How do I get set up? ###

* Clone the code from bitbucket and setup git for it
* You don't have to use any GUI app because PyCharm does have plugin for it but you can use SourceTree (which is recommended) for a better visual

### PostgreSQL installation

* Follow the instruction in this link for both Window and Mac https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/content/optional_postgresql_installation/
* After that, you can use the default database tool in Pycharm: View > Tool Windows > Database. 
* Add new Data Source as PostgreSQL. Host should be 'localhost'. Database name should be 'hmr_db'. URL should be 'jdbc:postgresql://localhost:5432/hmr_db'. 5432 is the port which you are using for PostgreSQL, may be different for each person.
* Then try test connection. If no error, you are good to go.


### Things need to be checked before committing code ###

* Review your code
* Make sure it doesn't make any error!!!
* Remember to writing unit tests for logic functions
* Rerun unit tests if you make any change involving logic
* Check your database USERNAME AND PASSWORD, comment it and leave the default on (in  Hmr/setting.py line 100)
* Last but not least, be careful to merge your code, don't override others!


### How to run C.A.K.E application on your local network (and any devices connected to it)

* First of all close all your running application on pycharm
* Open terminal and run:
    - ifconfig
* Write down your pc ip address (the line that starts with: inet 192.168.0.100 )
* Open the port 8000 of your router, to do so:
    - Go to your router admin page, usually http://192.168.0.1 or http://192.168.0.0 (check router webpage for more info)
    - Port forward-> ip = 192.168.0.100 => port (public) 8000-> (private) 8000
* On Pycharm go to:
    - Tools -> Run manage.py Task..
    - On the console write:
    - Runserver 0.0.0.0:8000
* Run it and from any device connected to the same network as your pc go to your pc-ip followed by port :8000:
    - http://192.168.0.100:8000