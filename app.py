from flask import Flask, render_template, make_response
import os
import socket
import fnmatch

app = Flask(__name__)


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]

@app.route('/')
def hello_world():
    template = render_template('index.html', ip=get_local_ip())
    return make_response(template)


@app.route('/widgetlist.xml')
def widget_list():
    folder = './static/widgets'
    widgets = {}
    for file in os.listdir(folder):
        if fnmatch.fnmatch(file, '*.zip'):
            widgets[file.split('.')[0].title()] = {'size': os.path.getsize(f'{folder}/{file}'), 'file_name': file}

    template = render_template('widgetlist.xml', widgets=widgets, ip=get_local_ip())
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
