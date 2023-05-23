import os
from flask import Flask, render_template, json
import json

app = Flask(__name__)

# define the directory containing your JSON files
json_directory = 'C:\\Users\\Henri\\Documents\\GitHub\\Project-Lawful-Audiobook\\src\\data\\board_chunks'

@app.route('/')
def index():
    # get a list of all JSON files in the directory
    # json_files = [f for f in os.listdir(json_directory) if f.endswith('.json')]
    json_files = sorted([f for f in os.listdir(json_directory) if f.endswith('.json')], key=lambda x: int(x.split('_')[2]))

    # return a template that displays the list of files
    return render_template('list.html', files=json_files)

@app.route('/view/<filename>')
def view_file(filename):
    # generate the full path to the file
    path = os.path.join(json_directory, filename)
    
    # load the JSON file
    with open(path) as f:
        data = json.load(f)
    
    # return a template that displays the content of the file
    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(port=5000, debug=True)