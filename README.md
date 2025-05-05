#The system is about a file managemnet system that has an ai that the user can interact with when accessing the selected file.
#There are 2 different models (in their own branch) each with the same concepts. The esaiest and most refined being model 1

#To run this file:

#~:Requirements

#1.pienv
#2. A running local llm on lm studio

#~Process:

#1.run "pipenv shell" to activate the virtual environment

#2.run "pipenv install" to install the required repositories

#3.run "python manage.py makemigrations python manage.py migrate" for the database migration

#4.run "python manage.py createsuperuser" to create the superuser

#5.run the aplication using "python manage.py runserver"

#6.to access the admin panel go to "/admin"
