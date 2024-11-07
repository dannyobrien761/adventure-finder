![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome Danny O'Brien,


## Gitpod Reminders

To run a frontend (HTML, CSS, Javascript only) application in Gitpod, in the terminal, type:

`python3 -m http.server`

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

To run a backend Python file, type `python3 app.py` if your Python file is named `app.py`, of course.

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

By Default, Gitpod gives you superuser security privileges. Therefore, you do not need to use the `sudo` (superuser do) command in the bash terminal in any of the lessons.

To log into the Heroku toolbelt CLI:

1. Log in to your Heroku account and go to *Account Settings* in the menu under your avatar.
2. Scroll down to the *API Key* and click *Reveal*
3. Copy the key
4. In Gitpod, from the terminal, run `heroku_config`
5. Paste in your API key when asked

You can now use the `heroku` CLI program - try running `heroku apps` to confirm it works. This API key is unique and private to you, so do not share it. If you accidentally make it public, you can create a new one with _Regenerate API Key_.

### Connecting your Mongo database

- **Connect to Mongo CLI on a IDE**
- navigate to your MongoDB Clusters Sandbox
- click **"Connect"** button
- select **"Connect with the MongoDB shell"**
- select **"I have the mongo shell installed"**
- choose **mongosh (2.0 or later)** for : **"Select your mongo shell version"**
- choose option: **"Run your connection string in your command line"**
- in the terminal, paste the copied code `mongo "mongodb+srv://<CLUSTER-NAME>.mongodb.net/<DBname>" --apiVersion 1 --username <USERNAME>`
  - replace all `<angle-bracket>` keys with your own data
- enter password _(will not echo **\*\*\*\*** on screen)_




## Contents:

- <a href="#ux">UX</a>
  - <a href="#strategy">Strategy</a>
  - <a href="#db">Database structure</a>
  - <a href="#design">Design</a>
- <a href="#testing">Testing</a>
- <a href="#bugs">Bugs</a>
- <a href="#features">Existing Features</a>
- <a href="#f_features">Features left to Implement</a>
- <a href="#technology">Languages, Technologies & Libraries</a>
- <a href="#credits">Credits</a>
- <a href="#deployment">Deployment</a>
- <a href="#acknowledgements">Acknowledgements</a>

## <div id="ux">UX</div>
### Overview
Adventure Finder is a vlog and blog app that allows users to  easily find adventures  within activities and locations they are interested in. the adventure finder app is a community of outdoor enthusiasts looking to find information about an outdoor activity, location, local businesses and be able comment or like on thier favorite posts. Magazine style operated with only featured user stories written by designated approved authors.

#### First Time User
- As a person who is interested in outdoor adventures.
- As a person who is looking for more information about an activity or location of interest.
- As a person who prefers to see videos of these activitites the business that run them and the location.

#### Returning User
- As a returning user, part of the adventure findr community.
- As a returning user, who already has an account I would like quickly and easily comment on posts and find out more information.
- As a returning user, I would like to see the newest adventures on the site so that I can find something new and interesting for myself (for example, new post).

### <div id="strategy">Strategy</div>
Determining the best approach meant studying the needs of potential users. This included similar sites research and taking inspiration

#### Agile
The Agile methodology was used to plan the project. Github was used as the tool to demonstrate this.  Issues were used to create User Stories with custom templates ([Link to Kanban board](https://github.com/users/dannyobrien761/projects/1/views/1)). 

#### Good Design practice
I separated the urls.py files into separate apps because, as stated, this follows the Django design philosophy of loose coupling. 
##### User Stories 
Issues were used to create User Stories with custom templates for admin and user. I added the acceptance criteria and the tasks so I can track my work effectively. Once I completed a User Story I would move it from `in progress` to `completed`. 

the acceptance criteria was formulated  from the card conversation and confirmation appraoch

- Completed User Stories:<br />

 

- Uncompleted User Stories:<br/>

    

  ---

  superuser created for django admin CRUD operations 


#### commwnt feature
class Comment(models.Model):
  author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')


The author field is set as null=True, blank=True, so it’s only populated if the commenter is an author.
This setup enables the app to differentiate between comments from authors and regular users


approved = models.BooleanField(default=False)

ensures that new comments are unapproved by default, making it easy to manage comment moderation.
This setup will let you handle comment approval efficiently, with all new comments defaulting to unapproved.