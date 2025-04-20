from flask import Flask, render_template, send_from_directory
from datetime import datetime

app = Flask(__name__, static_folder="assets")

@app.route('/')
def index():
    now = datetime.now()
    return render_template('index.html', current_year=now.year)

static_routes = {
    'countdown': {
        'path': '/var/www/mitchellshelton/countdown',
        'index_file': 'index.html'
    },
    'gan-scrambler': {
        'path': '/var/www/mitchellshelton/gan-scrambler',
        'index_file': 'index.html'
    }
}

for route, config in static_routes.items():
    path = config['path']
    index_file = config.get('index_file', 'index.html')

    def make_view(directory, default_file):
        def view(filename=default_file):
            return send_from_directory(directory, filename)
        return view

    app.add_url_rule(
        f'/{route}/',
        defaults={'filename': index_file},
        view_func=make_view(path, index_file),
        endpoint=f'{route}_index'
    )

    app.add_url_rule(
        f'/{route}/<path:filename>',
        view_func=make_view(path, index_file),
        endpoint=f'{route}_file'
    )
  
if __name__ == '__main__':
    app.run(debug=True)