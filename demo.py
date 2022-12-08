from datetime import datetime
from flask import Flask, render_template, request
from flask.views import View
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


app = Flask(__name__, static_folder='', template_folder='')
app.config['SECRET_KEY'] = 'secret'


class MyForm(FlaskForm):
    id = 'my_form'
    render_kw = {
        "hx-trigger": "keyup changed delay:1000ms",
        "hx-post": "/my_view",
        "hx-swap": "outerHTML",
        "hx-target": f"#{id}"
    }

    name = StringField('name', validators=[DataRequired()], render_kw=render_kw)
    prefix = StringField('prefix', render_kw=render_kw)

    @property
    def hello(self):
        return f"Hello {self.prefix.data or ''} {self.name.data or 'stranger'}"


class MyView(View):
    def render_form(self):
        form = MyForm(name="default")
        return render_template('my_form.html', form=form)

    def render_view(self):
        now = datetime.now()
        return render_template('my_view.html', view=self, now=now)

    def dispatch_request(self):
        htmx_target = request.headers.get('HX-Target')
        if htmx_target and htmx_target.endswith('form'):
            return self.render_form()
        return self.render_view()


app.add_url_rule('/my_view', view_func=MyView.as_view('my_view'), methods=['GET','POST'])
