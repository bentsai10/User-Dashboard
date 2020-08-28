# User Dashboard
A user management/messaging system for school clubs to engage users!

<p align = "center"><kbd><img src = "/images/dash.png" height = "400"></kbd></p>

<p><strong>User Dashboard's purpose:</strong><br> 
Provide an easy way for admin-level users to manage users on the platform and for all users to be able to interact via personal message boards </p>

<h3> Accessing User Dashboard</h3>
<ul>
  <li>Download this project from Github</li>
  <li>Make sure you have python3 installed</li>
  <li>Create a virtual environment and pip install django==2.2</li>
  <li>Navigate to project level folder in terminal and run "python manage.py runserver"</li>
  <li>Go to http://localhost:8000/ in your desired browser!</li>
  <li>Enjoy User Dashboard!</li>
</ul>

<h3>How User Dashboard Works</h3>
<ol>
  <li>Login to access the dashboard</li>
  <br>
  <p align = "center"><kbd><img src = "/images/login.gif"></kbd></p>
  
  <li>If you don't have an account, navigate to register for one!</li>
  <br>
 <p align = "center"><kbd><img src = "/images/register.gif"></kbd></p>
 <li>Both the login/register pages are equipped with validations to ensure data congruency</li>
  <br>
 <p align = "center"><kbd><img src = "/images/login_validations.gif"></kbd></p>
 <p align = "center"><kbd><img src = "/images/register_validations.gif"></kbd></p>
  <li>If you were the first user to register for an account, you are the admin of the site. Below is the admin view</li>
  <br>
  <p align = "center"><kbd><img src = "/images/admin_view.png"></kbd></p>
  <li>Regular users have access to the normal view below</li>
  <br>
  <p align = "center"><kbd><img src = "/images/normal_view.png"></kbd></p>
  <li>Personalize your profile by editing your name, email, and description</li>
  <br>
  <p align = "center"><kbd><img src = "/images/edit_profile.gif"></kbd></p>
  <p align = "center"><kbd><img src = "/images/edit_info.gif"></kbd></p>
  <p align = "center"><kbd><img src = "/images/edit_descrip.gif"></kbd></p>
  <li>Each user has their own page and message board, where other users can post messages or reply to existing messages</li>
  <br>
  <p align = "center"><kbd><img src = "/images/message_board.gif"></kbd></p>
  <li>Admins also have the ability to add new users, edit all users' info, and delete users</li>
  <br>
  <p align = "center"><kbd><img src = "/images/add_new_user.gif"></kbd></p>
  <p align = "center"><kbd><img src = "/images/delete_user_prompt.gif"></kbd></p>
  <li>When done using the platform, just logout!</li>
  <br>
  <p align = "center"><kbd><img src = "/images/logout.gif"></kbd></p>
</ol>
<h3>Logic Behind the Dashboard</h3>
<ul>
  <li>Database Models</li>
  <ul>
    <li>User: admin_level set to 9 if admin</li>
    <li>Post: two relationships with User, a poster and receiver. Receiver keeps track of which user's message board the post belongs to</li>
    <li>Comment: relationships with User and Post to keep track of poster and associated post, respectively</li>
  </ul>
  
```python3
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    user_level = models.IntegerField()
    password = models.CharField(max_length = 255)
    desc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
class Post(models.Model):
    content = models.TextField()
    poster = models.ForeignKey(User, related_name="posts_made", on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, related_name="posts_on_wall", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
  <li>Login/Register/Edit Validations</li>
  <ul>
    <li>Separate validator methods for each distinct situation: register, login, edit_info (name, email), edit_password</li>
    <li>Used EMAIL_REGEX to verify proper email format</li>
    <li>Used bcrypt to encrypt user password</li>
  </ul>
  
```python3
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if postData['password'] != postData['password_conf']:
            errors['password'] = "Your passwords don't match!"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        user = User.objects.filter(email=postData['email']) 
        if user:
            logged_user = user[0] 
            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                errors["password"] = "Incorrect password!"
        else:
            errors["email"] = "This email has not been registered!"
        return errors

    def edit_info_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters!"
        return errors

    def edit_password_validator(self, postData):
        errors = {}
        logged_user = User.objects.filter(email=postData['user']).all().first()
        if not bcrypt.checkpw(postData['old_password'].encode(), logged_user.password.encode()):
            errors["password"] = "Incorrect old password!"
        if len(postData['new_password']) < 8:
            errors['new_password'] = "New Password must be at least 8 characters!"
        if postData['new_password'] != postData['new_password_conf']:
            errors['new_password'] = "Your new passwords don't match!"
        return errors
```
  <li>Dashboard Template</li>
  <ul>
    <li>Use Bootstrap for styling across site</li>
    <li>Basic navbar containing useful site tabs (needs improvement, not entirely responsive)</li>
    <li>Various django template if statements to alter user view depending on user_level (admin or not) </li>
    <li>Django for loop to iterate through all users and display their info accordingly </li>
  </ul>

```html
...
    <head>
        ...
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <a class="navbar-brand" href="#">Test App</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse " id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item active">
                      <a class="nav-link" href="http://localhost:8000/dashboard">Home <span class="sr-only">(current)</span></a>
                    </li>
                    <li class="nav-item active">
                        <a class="nav-link" href="http://localhost:8000/users/edit">Edit Profile <span class="sr-only">(current)</span></a>
                    </li>
                </ul>
              <ul class="navbar-nav ml-auto">
                <li class="nav-item active">
                  <a class="nav-link" href="http://localhost:8000/logout">Logout<span class="sr-only">(current)</span></a>
                </li>
              </ul>
            </div>
        </nav>
        <div id = "header" class = "container" style = "display: flex; padding: 30px;">
            {% if current_user.user_level == 9 %}
                <h1 class = "display-4">Manage Users</h1>
                <a href="http://localhost:8000/users/new" class = "btn btn-outline-primary ml-auto" style = "font-size: 20px; height: 44px; margin-top: 16px;">Add New</a>
            {% else %}
            <h1 class = "display-4">All Users</h1>
            {% endif %}
        </div>
        <div class = "container">
            <table class = "table table-striped">
                <thead class = "thead-dark">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Created At</th>
                        <th>User Level</th>
                        {% if current_user.user_level == 9 %}
                        <th>Actions</th>
                        {% endif %}
                    </tr>
                </thead>
                <tbody>
                    {% for user in users %}
                    <tr>
                        <td>{{user.id}}</td>
                        <td><a href="http://localhost:8000/users/show/{{user.id}}">{{user.first_name}} {{user.last_name}}</a></td>
                        <td>{{user.email}}</td>
                        <td>{{user.created_at|date:'Y-m-d'}}</td>
                        <td>{% if user.user_level == 9 %} admin {% else %} normal {% endif %}</td>
                        {% if current_user.user_level == 9 %}
                        <td style = "display: flex;"><a href = "http://localhost:8000/users/edit/{{user.id}}" style = "margin-top: -8px;" class = "btn btn-link">Edit</a><form action="" method = "POST">{% csrf_token%}<button style = "margin-top: -8px;" class = "btn btn-link" onclick="confirm('Are you sure you want to delete this user?')">Delete</button></form>
                        {% endif %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
...
```
</ul>
