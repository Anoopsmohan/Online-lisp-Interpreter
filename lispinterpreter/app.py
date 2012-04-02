import web
from google.appengine.ext import db
import hashlib
import base64
from web import form
import lisp
import lispio
from lisp import *
Alist=[]

web.config.debug = False

urls = ('/', 'home',
'/signin.html','signin',
'/signup.html','signup',
'/tutorial','tutorial',
'/register_success', 'regsuccess',
'/signin_fail','signfail',
'/home.html','home',
'/signin_error1','signerror',
'/signin_after.html','signafter',
'/about_us.html','aboutus',
'/contact_us.html','contact',
'/examples.html','examples',
'/feed_back.html','feedback',
'/about.html','about')



render = web.template.render('templates/')
app = web.application(urls, globals(),True)

#store = web.session.DiskStore('sessions')
#session = web.session.Session(app,store,initializer={'login': 0,'privilege': 0})
#render = web.template.render('templates', globals={'context': session})


my_form = web.form.Form(
                web.form.Textarea('', class_='text_area3', id='textfield', cols="40", rows="6")
                )
class Data(db.Model):
    username = db.StringProperty()
    password = db.StringProperty()
    email = db.StringProperty()
    firstname = db.StringProperty()
    lastname = db.StringProperty()
    age = db.StringProperty()
    gender = db.StringProperty()
    country = db.StringProperty()

class Comments(db.Model):
    name = db.StringProperty()
    email = db.StringProperty()
    message = db.TextProperty()


class home:
    def GET(self):
	notes = db.GqlQuery("SELECT * FROM Comments WHERE name != 'Divya Anoop'")	
        count = notes.fetch(200)
	return render.home(count)

    def POST(self):
	cmts =  web.input()
        feedback = Comments()
	feedback.name=cmts.name
	feedback.email=cmts.email
	feedback.message=cmts.message
	feedback.put()
        raise web.redirect('/home.html')

#class signout:
 #   def GET(self):
	#session.kill()
#	return render.home()

class signin:
    def GET(self):
	return render.signin()

    def POST(self):
        fi =  web.input()
	notes = db.GqlQuery("SELECT * FROM Data " + "WHERE email = :1 AND password = :2", fi.email,fi.password)
        count=notes.fetch(8)     
        if len(count)!=0: 
           # session.loggedin = True
           # session.username = fi.email
            raise web.redirect('/tutorial')
        else:
            raise web.redirect('/signin_error1')

class signfail:
    def GET(self):
	return render.signin_fail()

    def POST(self):
        fi =  web.input()
	notes = db.GqlQuery("SELECT * FROM Data " + "WHERE email = :1 AND password = :2", fi.email,fi.password)
        count=notes.fetch(8)     
        if len(count)!=0: 
            #session.loggedin = True
           # session.username = fi.email
            raise web.redirect('/tutorial')
        else:
            raise web.redirect('/signin_fail')

class signerror:
    def GET(self):
	return render.signin_error1()

    def POST(self):
        fi =  web.input()
	notes = db.GqlQuery("SELECT * FROM Data " + "WHERE email = :1 AND password = :2", fi.email,fi.password)
        count=notes.fetch(8)
        if len(count)!=0: 
           # session.loggedin = True
           # session.username = fi.email
            raise web.redirect('/tutorial')
        else:
            raise web.redirect('/signin_fail')



class signup:
    def GET(self):
	return render.signup()

    def POST(self):
        fi =  web.input()
        signup = Data()
	signup.username=fi.username
	signup.password=fi.password
	signup.email=fi.email
	signup.firstname=fi.firstname
	signup.lastname=fi.lastname
	signup.age=fi.age
	signup.gender=fi.gender
	signup.country=fi.country
	signup.put()
        
        raise web.seeother('/register_success')

class regsuccess:
    def GET(self):
	return render.register_success()


class signafter:
    def GET(self):
	return render.signin_after()

    def POST(self):
	fi =  web.input()
	notes = db.GqlQuery("SELECT * FROM Data " + "WHERE email = :1 AND password = :2", fi.email,fi.password)
        count=notes.fetch(8)
        if len(count)!=0: 
        #    session.loggedin = True
         #   session.username = fi.email
            raise web.redirect('/tutorial')
        else:
            raise web.redirect('/signin_fail')
	

class tutorial:
    def GET(self):
        form = my_form()
        return render.tutorial(form, "Result")
        
    def POST(self):
	Alist=lisp.Alist
	global data1
	
        form = my_form()
        form.validates()
	#f = open('test.txt','w')
        data1 = form.value['textfield']
	
	#f.write(str(data1))
	try:
	    s=lispio.getSexp()
	except:
	    return "Invalid Input"
        #f.write(str(s))
	#f.close()
	try:
	    list1=lispio.putSexp(eval(s,Alist))
	#return str(list1)
	
	    return str(list1)
	except:
	    return "???"


class aboutus:
    def GET(self):
	return render.about_us()
    def POST(self):
	cmts =  web.input()
        feedback = Comments()
	feedback.name=cmts.name
	feedback.email=cmts.email
	feedback.message=cmts.message
	feedback.put()
        raise web.redirect('/about_us.html')



class contact:
    def GET(self):
	return render.contact_us()
    def POST(self):
	cmts =  web.input()
        feedback = Comments()
	feedback.name=cmts.name
	feedback.email=cmts.email
	feedback.message=cmts.message
	feedback.put()
        raise web.redirect('/contact_us.html')
 
class feedback:
    def GET(self):
   	notes = db.GqlQuery("SELECT * FROM Comments WHERE name != 'Divya Anoop' ")	
        count = notes.fetch(200)
	return render.feed_back(count)

    def POST(self):
	cmts =  web.input()
        feedback = Comments()
	feedback.name=cmts.name
	feedback.email=cmts.email
	feedback.message=cmts.message
	feedback.put()
        raise web.redirect('/feed_back.html')



class about:
    def GET(self):
        return render.about()

class examples:
    def GET(self):
	return render.examples()

main = app.cgirun()


