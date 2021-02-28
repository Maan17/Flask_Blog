from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

#setup of database
#parameter in app config is the path where database is stored
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

#each class variable is considered as a piece of data in the database
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #this function prints out whenever we create a blog post
    def __repr__(self):
        return 'Blog post ' + str(self.id)

@app.route('/')
def index():
    return render_template('index.html')

#if nothing is listed then only request allowed is get by default
@app.route('/posts',methods=['GET','POST'])
def posts():
    if request.method=='POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title,content=post_content, author=post_author)
        #below command adds data to the database only in the current session, change is volatile
        db.session.add(new_post)
        #this command saves the data permanently to the database
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted)
        return render_template('posts.html',posts=all_posts)
    return render_template('posts.html',posts=all_posts)

#base url(url of the website)
@app.route('/home/user/<string:name>')
@app.route('/home/<string:name>')#handling multiple routes with same method
def hello(name):
    return "<h1>Hello World,</h1>"+name

@app.route('/int/<int:id>')
def hello2(id):
    return "Hello World,"+str(id)

@app.route('/home/users/<string:name>/posts/<int:id>')
def hello3(name,id):
    return "Hello, "+name+ ",your id is: "+str(id)

#it will allow only the methods mentioned(use POST method to see the change)
@app.route('/onlyget',methods=['GET'])
def get_req():
    return 'You can only get this webpage. '

#defining new route for delete
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

#defining a new route for edit post
@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content  = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

#create a new route for new posts
@app.route('/posts/new',methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content  = request.form['content']
        new_post = BlogPost(title=post_title,content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_posts.html')


#if we are directly running the file from command line
#in that case the name will be main
if __name__=="__main__":
    #we should turn on the debug mode which makes error handling easy
    app.run(debug=True)