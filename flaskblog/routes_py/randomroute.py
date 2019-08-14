import pyscreenshot
from flaskblog import app
from flask import render_template
import secrets
import os

@app.route('/sorandomwhy', methods=['POST'])
def XD():
    im = pyscreenshot.grab()
    random_id = secrets.token_hex(8)
    file_name = 'static/{}.png'.format(random_id)
    im.save(file_name)
    #os.remove(os.path.join(app.root_path, 'static', file_name))
    return render_template('show.html', screenshot=file_name)