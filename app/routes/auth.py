from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.forms.auth import LoginForm, RegistrationForm, ProfileInfoForm, ChangePasswordForm
from app import db
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('用户名不存在', 'error')
        elif not user.check_password(form.password.data):
            flash('密码错误', 'error')
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            flash('登录成功！欢迎回来', 'success')
            return redirect(next_page)
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功退出登录', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # 检查用户名是否已存在
        if User.query.filter_by(username=form.username.data).first():
            flash('用户名已被注册', 'error')
            return render_template('auth/register.html', form=form)
        
        try:
            user = User(
                username=form.username.data,
                real_name=form.realname.data,
                phone=form.phone.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('注册成功！请登录', 'success')
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
            flash('注册失败，请重试', 'error')
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    info_form = ProfileInfoForm()
    password_form = ChangePasswordForm()
    
    # 处理 AJAX 请求
    if request.is_json:
        data = request.get_json()
        if data.get('set_form_type'):
            session['form_type'] = data['form_type']
            return {'status': 'success'}
        elif data.get('clear_form'):
            session.pop('form_type', None)
            return {'status': 'success'}
    
    # 如果是直接访问页面（GET 请求），清除表单状态
    if request.method == 'GET' and not request.is_json:
        session.pop('form_type', None)
    
    form_type = session.get('form_type')
    
    if info_form.submit.data and info_form.validate():
        try:
            current_user.real_name = info_form.realname.data
            current_user.phone = info_form.phone.data
            db.session.commit()
            flash('个人信息更新成功', 'success')
            session.pop('form_type', None)  # 成功后清除状态
        except:
            db.session.rollback()
            flash('更新失败，请重试', 'error')
    
    if password_form.submit.data and password_form.validate():
        if not current_user.check_password(password_form.old_password.data):
            flash('当前密码错误', 'error')
        # 检查新密码是否与原密码相同
        elif current_user.check_password(password_form.password.data):
            flash('新密码不能与当前密码相同', 'error')
        else:
            try:
                current_user.set_password(password_form.password.data)
                db.session.commit()
                flash('密码修改成功', 'success')
                session.pop('form_type', None)  # 成功后清除状态
            except:
                db.session.rollback()
                flash('修改失败，请重试', 'error')
    
    if not info_form.is_submitted():
        info_form.realname.data = current_user.real_name
        info_form.phone.data = current_user.phone
    
    return render_template('auth/profile.html', 
                         info_form=info_form, 
                         password_form=password_form,
                         form_type=form_type)  # 传递表单状态到模板 