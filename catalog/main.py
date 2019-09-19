from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from project_database import Register,Base,User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_login import LoginManager,login_user,current_user,logout_user,login_required,UserMixin

engine=create_engine('sqlite:///iii.db',connect_args={'check_same_thread':False},echo=True)
#engine=create_engine('sqllite:///iii.db')
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()


app=Flask(__name__)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'



app.config['MAIL_SERVER']="smtp.gmail.com"
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='saisushmithavarma30@gmail.com'
app.config['MAIL_PASSWORD']="@@@@@@@@@@@"
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

app.secret_key='abc'

mail=Mail(app)
otp=randint(000000,999999)



@app.route("/sample")
def demo():
   return  "Welcome APSSDC to IIIT nuzvid "

@app.route("/demo")
def d():
    return "<h1>Welcome to my world</h1>"

@app.route("/info/details")
def de():
    return("Hello Details")

@app.route("/details/<name>/<fname>")
def info(name,fname):
    #return "hello {}".format(name)
    
    return "hello {} and {}".format(name,fname)

@app.route("/detailsinfo/<name>/<int:age>/<float:salary>")
def infor(name,age,salary):
   
    
    return "My name is {} and my age is {} my salary is  {}".format(name,age,salary)


#url_for and redirect

@app.route("/admin")

def admin():
    return "Hello I am an Admin"

@app.route("/student")

def student():
    return "Hello I am a student"


@app.route("/staff")

def staff():
    return "Hello I an Staff"




@app.route("/information/<name>")

def admin_info(name):
    if name=='admin':
        return redirect(url_for('admin'))
    elif name=='student':
        return redirect(url_for('student'))
    elif name=='staff':
        return redirect(url_for('staff'))
    else:
        return "No Url"
    
@app.route("/data")
def demo_html():
    return render_template('samplee.html')

@app.route("/data/<name>/<int:age>/<float:salary>")
def demo_html1(name,age,salary):
    return render_template('sample.html',n=name,a=age,s=salary)



@app.route("/info_data")
def info_data():
    sno=47
    name='Sushmitha'
    branch='IT'
    dept='Trainer'
    return render_template('tabledata.html',s_no=sno,n=name,b=branch,d=dept)



adata=[{'sno':123,'name':'shivaram','branch':'Medicine','dept':'Marketing'},{'sno':47,'name':'Sushmitha','branch':'IT','dept':'CSE'}]

@app.route("/dataset1")
def dummy():
        return render_template('tabledata.html',dummy_data=adata)


@app.route("/data2/<int:number>")
def table5(number):
     return render_template('table5.html',n=number)


#File Upload
@app.route("/file_upload",methods=['GET','POST'])
def file_upload():
    return render_template("file_upload.html")

@app.route("/success",methods=['GET','POST'])
def success():
    if request.method=='POST':
        f=request.files['file']
        f.save(f.filename)
        return render_template("success.html",f_name=f.filename)



#Email sending and Otp generation

@app.route("/email")
def email_send():
    return render_template("email.html")

@app.route("/email_verify",methods=['POST','GET'])
def verify_email():
    email=request.form['email']
    msg=Message('One Time Password',sender='saisushmithavarma30@gmail.com',recipients=[email])
    msg.body=str(otp)
    mail.send(msg)
    return render_template("v_email.html")

@app.route("/email_success",methods=['POST','GET'])
def success_email():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        return render_template("email_success.html")
    return "Invalid OTP"


#Create and update     
@app.route("/show")
@login_required
def showData():
    register=session.query(Register).all()
    return render_template('show.html',reg=register)

@app.route("/loginpage",methods=['POST','GET'])
def login():
    if request.method=='POST':
        newData=Register(name=request.form['name'],
                        surname=request.form['surname'],
                        mobile=request.form['mobile'],
                        email=request.form['email'],
                        branch=request.form['branch'],
                        role=request.form['role'])
        session.add(newData)
        session.commit()
        flash("New Data Added")

        return redirect(url_for('showData'))
    else:
        return render_template('login_page.html')

@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editData(register_id):
    editedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':  
        editedData.name=request.form['name'] 
        editedData.surname=request.form['surname'] 
        editedData.mobile=request.form['mobile'] 
        editedData.email=request.form['email'] 
        editedData.branch=request.form['branch'] 
        editedData.role=request.form['role'] 

        session.add(editedData)
        session.commit()
        flash("Data is edited{}".format(editedData.name))
        return redirect(url_for('showData'))
    else:
        return render_template('edit.html',register=editedData)

@app.route("/delete/<int:register_id>",methods=['POST','GET'])
def deleteData(register_id):
    deletedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':  
        session.delete(deletedData)
        session.commit()
        flash("Data is deleted{}".format(deletedData.name))
        return redirect(url_for('showData'))
    else:
        return render_template('delete.html',register=deletedData)

#Index page started
@app.route("/account",methods=['POST','GET'])
@login_required
def account():
    return render_template('account.html')

@app.route("/register",methods=['POST','GET'])
def reg():
    if request.method=='POST':
        userData=User(name=request.form['name'],
                     email=request.form['email'],
                     password=request.form['password'])
        session.add(userData)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('register.html')


@login_required
@app.route("/login",methods=['POST','GET'])  
def loginn():
    if current_user.is_authenticated:
        return redirect(url_for('showData'))
    try:
        if request.method=='POST':
            user=session.query(User).filter_by(email=request.form['email'],password=request.form['password'].first())
            if user:
                login_user(user)
                return redirect(url_for('showData'))
            else:
                flash("Invalid Login")
        else:
            return render_template('login.html',title="login")
    except Exception as e:
        flash("Login Failed...")
    else:
        return render_template('login.html',title='login')

@app.route("/logout")
def logout():
    logout_user()
    return render_template(url_for('index'))
@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

@app.route("/")
def index1():
    return render_template('index.html')




  

    




































    
if __name__=="__main__":
    app.run(debug=True)