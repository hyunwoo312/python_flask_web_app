from flaskblog import app
from flask import render_template, abort

@app.route('/protected/<path:filename>')
def disable_traffic(filename):
    abort(401)

@app.errorhandler(404)
def page_not_found404(e):
    return render_template('etc/error.html', title='( ゜Д゜；)！？ the page you are looking for could not be found. - Aniani')

@app.errorhandler(403)
def page_not_found403(e):
    return render_template('etc/error.html', title='((((｡(´°Α°｀)｡)))) you have no access - Aniani')

@app.errorhandler(405)
def page_not_found405(e):
    return render_template('etc/error.html', title='☆ｏ(＞＜；)○ you have no access!!- Aniani')

@app.errorhandler(401)
def page_not_found666(e):
    return render_template('etc/angry.html', title='(╬ಠ益ಠ)(╬ಠ益ಠ)(╬ಠ益ಠ) - Aniani')