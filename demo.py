import jinja2
from flask import Flask, render_template, request
# from flask_wtf import FlaskForm
from wtforms import Form, StringField
from wtforms.validators import DataRequired


app = Flask(__name__, static_folder='', template_folder='')


class HTMXForm:
    def __init__(self, *args, **kwargs):
        super(HTMXForm, self).__init__(*args, **kwargs)

    def render(self):
        return jinja2.utils.markupsafe.Markup(render_template(self.template, form=self))


class MyForm(HTMXForm, Form):
    id = 'my_form'
    template="my_form.html"
    render_kw = {
        "hx-trigger": "keyup changed delay:1000ms",
        "hx-post": "/wtforms_htmx",
        "hx-swap": "outerHTML",
        "hx-target": f"#{id}"
    }

    name = StringField('name', validators=[DataRequired()], render_kw=render_kw)
    prefix = StringField('prefix', render_kw=render_kw)

    @property
    def hello(self):
        return f"Hello {self.prefix.data or ''} {self.name.data or 'stranger'}"


@app.route("/wtforms_htmx", methods=['POST'])
def wtforms_htmx():
    form = MyForm(formdata=request.form)
    return form.render()


@app.route('/my_form', methods=['GET', 'POST'])
def my_form():
    form = MyForm(name="default")
    # if form.validate_on_submit():
    #     return redirect('/my_form')
    return render_template('demo.html', form=form)
