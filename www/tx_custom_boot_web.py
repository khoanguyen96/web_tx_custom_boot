import flask
import hekate
from .builder import CachedBuilder

app = flask.Flask(__name__)

@app.route('/')
def index():
  h = hekate.GithubHekate()
  releases = h.list_named_hekate_releases()

  return flask.render_template('index.html', releases=releases)

@app.route('/download')
def build_download():
  version = flask.request.args.get('version')

  if version is None:
    return flask.abort(404)

  try:
    r_id = int(version)
    boot_file = CachedBuilder().get(r_id)

    if boot_file:
      return flask.send_file(str(boot_file), as_attachment=True, attachment_filename="boot.dat")
    else:
      flask.flash('Uh oh! Selected version was not found!')
      return flask.redirect(flask.url_for('index'))
  except:
    flask.flash('Uh oh! An unexpected error occurred!')
    return flask.redirect(flask.url_for('index'))