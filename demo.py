from uuid import uuid4
from blinker import Namespace
import jinja2
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
# from flask_wtf import FlaskForm
from werkzeug.datastructures import MultiDict
from wtforms import Form, StringField
from wtforms.validators import DataRequired


app = Flask(__name__, static_folder='', template_folder='')
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
forms = dict()
signals = Namespace()


class OnlineForm:
    def __init__(self, *args, oid=None, template=None, **kwargs):
        super(OnlineForm, self).__init__(*args, **kwargs)

        oid = str(uuid4()) if oid is None else oid
        self.oid = oid
        forms[oid] = self

        self.template = template

    def render(self):
        return jinja2.utils.markupsafe.Markup(render_template(self.template, form=self))


class MyForm(OnlineForm, Form):
    name = StringField('name', validators=[DataRequired()])

    @property
    def hello(self):
        return f"Hello {self.name.data}"


@app.route('/my_form', methods=['GET', 'POST'])
def my_form():
    form = MyForm(name="default", template="my_form.html")
    # if form.validate_on_submit():
    #     return redirect('/my_form')
    return render_template('demo.html', form=form)


@socketio.on('change')
def handle_socket_change(event):
    oid = event['oid']
    form = forms[oid]

    name = event['name']
    value = event['value']
    data = MultiDict([(name, value)])
    form.process(data)

    signals.signal('change').send(form)


# FIXME: fix event loop
@signals.signal('change').connect
def handle_signal_change(form):
    oid = form.oid
    html = form.render()
    emit('update', dict(oid=oid, html=html))


if __name__ == '__main__':
    socketio.run(app)
