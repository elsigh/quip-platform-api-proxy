
quip-platform-api-proxy
====

This repo represents a pretty basic server running on heroku that can make calls to the Quip Automation API given a token.


Install instructions
----

- Step 1: Copy https://github.com/quip/quip-api/blob/master/python/quip.py into this directory
- Step 2: `pip install -r requirements.txt`
- Step 3: `python server.py` should start the server at http://0.0.0.0:8080/

In the Quip Feedback live app you can point the `API_PROXY` at localhost to test and view logs interactively.

Use `git push origin heroku` to deploy to heroku


