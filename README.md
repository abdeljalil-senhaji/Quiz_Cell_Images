# **Tutorial**

BioQ is a playful learning website, you will learn how to recognise microscopy features and components by answering quiz.

## Link to the web site:
https://cryptic-plains-80674.herokuapp.com/BioQ/


## Advantages of the application:

- The web pages where developed using bootstrap which gives an adaptative (responsive) form, for the web and for the mobile.
- jQuery is used to sort data, for the icon and for ajax.
- Different categories of quiz with different levels.
- Possibility to explore data (sort/filter)


## Installation

### Run in local:

Download all the files in the directory `projet_django ` , go to console:

- Create an environement:

`conda create --name djangoenv python=3.7`


`Activate conda enviroment`


`conda activate djangoenv`

- Install packages


`conda install --name djangoenv django==3.0.3`

`conda install --name djangoenv sqlparse==0.3.1`

- Send to server:

`cd projet_django`

`python manage.py runserver`





### Home page

The home page should look like this once you run the server.

![Home page](Image/homePage.gif)


## Registration 

Click on the 'register' button to create an account.

![registration page](Image/registration.gif)


## login

Click on 'login' button to log in.
Once you log in, you will be redirected to the following page:


![login page](Image/login_logout.gif)


You can select Quiz 1 or Quiz 2:


## Quiz 1

If you pick Quiz 1 you will see 3 images and you will have to tell with
which kind of microscopy the images were obtained. 


Before getting in the quiz  choose a level you will be redirected to the Quiz:

here's an example:


you have 4 possibilities to answer:


if you select the correct answer you obtain 1 point:



if you give a bad answer, you do not obtain any point 


![quiz1 page](Image/quizz1.gif)


## Quiz 2

If you pick Quiz 2 you will see  2 images and you will have to tell to which component they belong.



here's an example:


you have 4 possibilities to answer:








if you select the correct answer you obtain 3 points:





if you give a bad answer, you do not obtain any point

![quizz2 page](Image/quizz2.gif)


## Explore:

You have the possiility to explore data, search and sort each column.


![explore page](Image/explore.gif)

