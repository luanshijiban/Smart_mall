from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, Optional
from app.models.user import User

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=30, message='用户名长度必须在3-30之间')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, message='密码长度不能小于6位')
    ])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录') 

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'),
        Length(min=3, max=20, message='用户名长度必须在3-20个字符之间'),
        Regexp(r'^[\w]+$', message='用户名只能包含字母、数字和下划线')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码'),
        Length(min=6, max=20, message='密码长度必须在6-20个字符之间'),
        Regexp(r'^[\w@#$%^&+=]+$', message='密码只能包含字母、数字和特殊字符(@#$%^&+=)')
    ])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    realname = StringField('真实姓名', validators=[
        Length(max=60, message='姓名长度不能超过60个字符')
    ])
    phone = StringField('联系电话', validators=[
        Optional(),
        Length(max=20, message='电话长度不能超过20个字符'),
        Regexp(r'^\d*$', message='电话号码只能包含数字')
    ])
    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用')

class ProfileInfoForm(FlaskForm):
    """修改个人信息表单"""
    realname = StringField('真实姓名', validators=[
        Length(max=60, message='姓名长度不能超过60个字符')
    ])
    phone = StringField('联系电话', validators=[
        Length(max=20, message='电话长度不能超过20个字符'),
        Regexp(r'^\d+$', message='电话号码只能包含数字')
    ])
    submit = SubmitField('保存修改')

class ChangePasswordForm(FlaskForm):
    """修改密码表单"""
    old_password = PasswordField('当前密码', validators=[
        DataRequired(message='请输入当前密码')
    ])
    password = PasswordField('新密码', validators=[
        DataRequired(message='请输入新密码'),
        Length(min=6, max=20, message='密码长度必须在6-20个字符之间'),
        Regexp(r'^[\w@#$%^&+=]+$', message='密码只能包含字母、数字和特殊字符(@#$%^&+=)')
    ])
    password2 = PasswordField('确认新密码', validators=[
        DataRequired(message='请确认新密码'),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    submit = SubmitField('修改密码')