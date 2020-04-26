![Python application](https://github.com/kirylvolkau/Python-Level-Up/workflows/Python%20application/badge.svg)
- Project link : https://daftcode-kvolkau.herokuapp.com
- Course repo link : https://github.com/daftcode/daftacademy-python_levelup-spring2020
- [Recruitment folder](/0_recruitment) : recruitment task on dynamic programming.

## Part 1 : D as "Deploy"
The main idea of this part tasks was to write simple web app in `python` and deploy it to Heroku with automatic deployment enabled. <br>
The trickiest part was to understand, that `uviciorn` for optimization purposes forks application, because web services should be stateless. In such situation global variables used for counting would be reset. As a solution was to decrease performance by blocking forking, but having only one instance of application running OR implement some kind of database with create and read functionality. I chose the second one with `storage.csv` file as a database.<br>
**Note** : "surename" is a misspelling in unit tests provided for us on `repl.it`.
## Part 2 : A as "Art"
Those tasks were about understanding idea of decorators in python and creating decorators, similar to which we will use later in our web-app. 
<br>
## Part 3 : F as "Feature"
- added BasicAuth.
- added `login` and `logout` endpoints (method : `POST`).
- added templates : Jinja2Templates.
- added decorator `is_logged_in` checking, if request contains cookie "session_token".
