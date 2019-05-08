# MovieAggregator
Basic movie database interacting with external API


# Usage
Clone This Project (Make Sure You Have Git Installed)
``
https://github.com/mustafamuratcoskun/DjangoBlogApp.git
``
Install Dependencies 

``
pip install -r requirements.txt
``

Set Database (Make Sure you are in directory same as manage.py)
``
python manage.py makemigrations
python manage.py migrate
``

After all these steps , you can start testing and this project. 

# Testing

Runserver:
``
python manage.py runserver
``
Movie Api
``
http://localhost:8000/movie/
``
Comment Api
``
http://localhost:8000/comments/
``
Top Movie Api:
``
http://localhost:8000/top/
``
