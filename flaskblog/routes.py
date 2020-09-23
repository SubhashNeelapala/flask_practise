
from flask import render_template,url_for,flash,redirect,request,abort
from flaskblog import app,db,bcrypt
from flaskblog.forms import RegistrationForm,LoginForm,UpdateAccountForm,PostForm
from flaskblog.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
# import secrets
import os
# posts = [{
#     'author':'Subhash',
#     'name':'first blog',
#     'created_at':'June 10 2020',
#     'content':'Sample title'
#     },
#     {
#     'author':'Satish',
#     'name':'first blog',
#     'created_at':'June 11 2020',
#     'content':'Sample title'
#     }
# ]

@app.route('/')
@app.route('/home')
def home_page():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page,per_page=2)
    return render_template('home.html',posts=posts)
    
@app.route('/about')
def about_page():
    return render_template('about.html',title='About')

@app.route('/registration',methods = ['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created for {}'.format(form.username.data),'success')
        return redirect(url_for('login'))
    return render_template('registration.html',title='Registration',form=form)

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            # print next_page
            return redirect(next_page) if next_page else redirect(url_for('home_page'))
        else:    
            flash('Loggin failed due to invalid credentials','danger')
    return render_template('login.html',title='Login',form=form)

@app.route('/logout',methods=['POST','GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _,f_ext = os.path.splitext(form.picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
#     form_picture.save(picture_path)
#     return picture_fn


@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated successfully')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)

@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(name=form.name.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been saved','success')
        return redirect(url_for('home_page'))
    return render_template('create_post.html',title="New Post",form=form,legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.name,post=post)

@app.route("/post/<int:post_id>/update",methods=['GET','POST'] )
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.name = form.name.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.name.data = post.name
        form.content.data = post.content
    return render_template('create_post.html',title='Update Post',form=form,legend='Update Post')
@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted','warning')
    return redirect(url_for('home_page'))

@app.route('/')
@app.route('/user/<string:username>')
def user_post(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
    .order_by(Post.created_at.desc())\
    .paginate(page=page,per_page=2)
    return render_template('user_post.html', posts=posts, user=user)



    select * from masters_location where subfacility_code in ('1146','1178','1179','1145','1148','1149','1154','1155','1165','1166','1167','1168','1169','1170','1171','1172','1173','1174','1175','1176','1177','1180','1181','1182','1183','1184','1185','1186','1187','1188','1189','1190','1191','1192','1193','1194','1195','1196','1197','1198');

