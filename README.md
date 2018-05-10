# vectorq-data

This small Flask app will provide a place to upload and retrieve collected
cosmic ray data.

## Config Options

There is a config file that needs to be set with the environment variable
__VECTORQ\_SETTINGS__. This config file only has two available options:

* DATA_DIR = "/path/to/data"

This is the location of the stored raw data files. For now, this is both
where the files are uploaded and retrieved.

* DEBUG = True or False

Set the DEBUG value to True or False to print out debugging messages. There's
not much in the way of custom debugging messages now, but if you wanted to
add some with:

```python
app.logger.debug("message")
```

Then setting DEBUG to True will make those messages get displayed on the
console.

## Running the App

You can run the app locally with flask by running it in a shell (in the same
directory as this repo). You can consult the official Flask [documentation](http://flask.pocoo.org/docs/0.12/quickstart/)
on how to get started, but below are the steps you should need to follow:

```bash
[~/vectorq-data]$ export FLASK_APP=vectorq-data.py
[~/vectorq-data]$ export VECTORQ_SETTINGS=vectorq-data.conf
[~/vectorq-data]$ flask-3 run
 * Serving Flask app "vectorq-data"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

If successful, the app will be running and listening at the address shown.
You can access that URL (http://127.0.0.1:5000/) in your web browser to
access the app, though you won't get a whole lot out of it.

If you encounter errors, ensure that the __FLASK\_APP__ and 
__VECTORQ\_SETTINGS__ values are set. Also ensure that your data directory (see
the [#config-options](Config Options) section) exists before starting the app.

## Endpoints

You can only make two kinds of requests to this app:

1. HTTP GET /get/&lt;resource&gt;

&lt;resource&gt; should be replaced with the filename you're looking for. It
the app will search for it in the __DATA\_DIR__ path on the server.

2. HTTP POST /set/&lt;resource&gt;

This creates a file in the __DATA\_DIR__ whose name matches &lt;resource&gt;. If
successful, you should be able to immediately retrieve it again with HTTP GET
at the /get/&lt;resource&gt; path instead of the "/set/..." path.

## Testing

Since this app is really just meant to take uploaded data and spit out existing
data, it might be more useful to test it on the command line.

If you know the "/get/..." path for a specific file, you can make that request
in your web browser. Uploading data is a little harder though.

For my own tests, I used wget on the command line:

```bash
[~]$ # at this point, we should have our flask app already running
[~]$ echo "0123456789ABCDEF 0123456789ABCDEF" > test.raw
[~]$ echo "1123456789ABCDEF 1123456789ABCDEF" >> test.raw
[~]$ echo "2123456789ABCDEF 2123456789ABCDEF" >> test.raw
[~]$ wget -O /dev/null --post-data="raw_data=$(cat test.raw)" http://localhost:5000/set/test.raw
--2018-05-10 10:46:15--  http://localhost:5000/set/a
Resolving localhost (localhost)... ::1, 127.0.0.1
Connecting to localhost (localhost)|::1|:5000... failed: Connection refused.
Connecting to localhost (localhost)|127.0.0.1|:5000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 24 [text/html]
Saving to: ‘/dev/null’

/dev/null                                       100%[======================================================================================================>]      24  --.-KB/s    in 0s      

2018-05-10 10:46:15 (4.35 MB/s) - ‘/dev/null’ saved [24/24]
```

Your output should show "200 OK" somewhere in your command if it was successful.
