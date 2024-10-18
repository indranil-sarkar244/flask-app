from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) #is creating an instance of the Flask class.
# __name__variable is a special built-in Python variable. It holds the name of the current Python module (i.e., the file that is being executed).


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" #This configuration key tells Flask-SQLAlchemy where the database is located and what type of database it is using. In this case, it is specifying a SQLite database.
#This will create a SQLite database named todo.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Setting this to False disables a feature that tracks object changes in SQLAlchemy and sends signals to the application when changes are made.
app.config['SQLALCHEMY_ECHO']=True #This is a configuration option for SQLAlchemy, a popular ORM (Object Relational Mapper) used to interact with databases in Python.
#When set to True: SQLAlchemy will log all the raw SQL statements it generates and executes.


db=SQLAlchemy(app)  #The line db = SQLAlchemy(app) initializes SQLAlchemy, a database toolkit, with your Flask app. It links the Flask app to SQLAlchemy, allowing you to manage database operations (like creating tables, inserting, updating, or querying data)
#using Python objects instead of raw SQL. The db object is used throughout the app to define models (tables) and interact with the database.

class Todo(db.Model):#  db.Model is a base class provided by SQLAlchemy.
 #When you write class Todo(db.Model), you're inheriting from db.Model, which means your Todo class becomes a SQLAlchemy
 #  model. This aenables the class to map to a table in the database.
 
    Sno=db.Column(db.Integer, primary_key=True)
    Title=db.Column(db.String(200), nullable=False)
    Desc=db.Column(db.String(500), nullable=False)
    Date_created=db.Column(db.DateTime, default=datetime.utcnow)#datetime.utcnow is a function from Python's datetime module that returns the current time in Coordinated Universal Time (UTC), which is a time standard that isn't affected by time zones or daylight saving changes.


    def __repr__(self) -> str:
        return f"{self.Sno} - {self.Title} "#The __repr__(self) method provides a human-readable string representation of an object. In this case, it returns the Sno (serial number) and Title of a Todo object in the format "{Sno} - {Title}". This makes it easier to identify and inspect objects 
    #during debugging or when printing them.

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=="POST":
        title=request.form["title"]#request.form object in Flask contains the submitted form data. The ["title"] part refers to the input field in the form that has the name title. This value is then stored in the title variable.
        desc=request.form["desc"]#Similarly, this line extracts the value of the form input with the name attribute desc. The desc variable stores whatever the user entered into the input field with this name.
        todo=Todo(Title=title, Desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    query=request.args.get('query')#request.args contains the data sent in the URL when a user submits the search form.
#.get('query') looks for the specific key named query in that data. If the user has entered something in the search bar, it retrieves that value; otherwise, it returns None.
    if query:
        allTodo=Todo.query.filter(Todo.Title.contains(query)|Todo.Desc.contains(query)).all()#Todo.query starts a query to access the Todo table in the database.
#.filter(...) adds a condition to the query.
#Todo.Title.contains(query) checks if the title of a todo item contains the search term (query).Todo.Desc.contains(query) checks if the description of a todo item contains the search term.
#.all() executes the query and returns all matching todo items as a list.
    else:
        allTodo=Todo.query.all()#simply fetches every record from the Todo table.

    return render_template('index.html', allTodo=allTodo)
   # return 'Hello, World!'



@app.route('/update/<int:Sno>', methods=['GET', 'POST'])
def update(Sno):
    if request.method=='POST':
        title=request.form["title"]
        desc=request.form["desc"]
        todo=Todo.query.filter_by(Sno=Sno).first()
        todo.Title=title
        todo.Desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo=Todo.query.filter_by(Sno=Sno).first()#this line is fetching and displaying the already submited 
    #data so it  would be easy for the user to update a particular thing in the submited data
    return render_template('update.html', todo=todo)#this render to the update.html and passes todo object


@app.route('/delete/<int:Sno>')
def delete(Sno):
    #allTodo= Todo.query.all()#This is a query using SQLAlchemy's ORM (Object Relational Mapper)
    #Todo.query is an object that allows querying the Todo model, which represents the todo table in the SQLite database.
    #.all() is a method that fetches all records from the todo table and returns them as a list of Todo objects.
   # print(allTodo) #This line prints the list of Todo objects to the terminal/console. Each object will be displayed according to the format defined in the __repr__ method, i.e., Sno - Title.
    todo=Todo.query.filter_by(Sno=Sno).first()#This line of code queries the Todo table for the first record where the Sno column matches the value of the Sno variable, 
    #and stores that record in the todo variable. If no such record is found, todo will be None.
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")



@app.route('/delete_all', methods=['GET','POST'])
def delete_all_todos():
    try:
        db.session.query(Todo).delete()
        db.session.commit()
        print("Done")
        return redirect("/")
    except Exception as e:
        db.session.rollback()
        return " An error occured " 
    
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000)#we can change the port number like this and
    #debug=true means if any bug is there show me on browser