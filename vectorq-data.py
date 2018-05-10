#!/usr/bin/env python3

import flask

import logging

import os.path

import re


# TODO: Make the test for a "resource_id" more meaningful
# This should match what you would expect for a valid data filename.
def _validate_resource_id(resource_id):
    re_c = re.compile(r"^[A-Za-z0-9\.]")
    m = re_c.match(resource_id)

    return m is not None

def _validate_contents(contents):
    # Test if the contents are ASCII text
    if len(contents) != len(contents.encode()):
        return False

# TODO: Change this REGEX to something more meaningful
# We might need to check multiple regular expressions if we can't
# express all line format variants with a single regular expression
    re_c = re.compile(r"^(?P<first_value>[0-9A-F]+)\s+(?P<second_value>[0-9A-F]+)")
    for line in contents.split('\n'):
        m = re_c.match(line)

        # No match means there's some corruption in the file, so
        # we'll just quit
        if m is None:
            return False

    return True

app = flask.Flask(__name__)
app.config.from_envvar("VECTORQ_SETTINGS")


# Do some initialization checking before getting started
def app_startup(app):
    if ('DATA_DIR' not in app.config.keys()):
        app.logger.error("No DATA_DIR value was set in the config")
        flask.abort(500)

    if os.path.exists(app.config['DATA_DIR']) == False:
        app.logger.error("No DATA_DIR path (%s) exists" %
                         (app.config['DATA_DIR']))
        flask.abort(500)

    if app.config['DEBUG']:
        app.logger.setLevel(logging.DEBUG)

app_startup(app)

# This route allows requests to retrieve a resource
# (eg. a raw data file)
# TODO: You might want to try to give a more verbose
# errors when they occur.
# There also might be other error cases that aren't accounted for here.
@app.route('/get/<resource_id>')
def get_data(resource_id):
    data_dir = app.config['DATA_DIR']

    contents = ''

# Client is asking for a bad resource ID value
    if not _validate_resource_id(resource_id):
        return flask.abort(400)

    if not os.path.exists(data_dir + "/" + resource_id):
        return flask.abort(404) #?

    with open(data_dir + "/" + resource_id, 'r') as f:
        contents = f.read()

    return contents


# This route accepts new input
# We declare the resource_id (which is essentially just the filename we want
# to use for storage) in the URI, but we could specify that in the POST
# data contents as well.
# The actual file contents get included in the raw_data POST value
@app.route('/set/<resource_id>', methods=['POST'])
def put_data(resource_id):
    data_dir = app.config['DATA_DIR']

# Client is asking for a bad resource ID value
    if not _validate_resource_id(resource_id):
        return flask.abort(400)

    if not _validate_contents(flask.request.values['raw_data']):
        # HTTP 400 - Bad Request
        return flask.abort(400)

    try:
        # Test os.path.exists(data_dir + "/" + resource_id)
        # If it already exists, do we overwrite or complain to the user?
        with open(data_dir + "/" + resource_id, 'w') as f:
            f.write(flask.request.values['raw_data'])
    except Exception as e:
        # Something went wrong writing the file
        # so we return a 500 - Internal Server Error
        app.logger.error("Error writing data file: %s" % (str(e)))
        flask.abort(500)

# TODO: Give a more meaninful success message?
    return "Upload for '{resource_id}' succeeded".format(resource_id=resource_id)

def main():
    # TODO: Unittests?
    pass

if __name__ == '__main__':
    main()
