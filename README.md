# CNAME shovel
In goes a list of URLs, out comes a list of CNAMEs for hostnames found in the rendered URLs.

### Requirements

* Python 2.7
* `selenium` and `dnspython` python packages
* PhantomJS web driver for Selenium

### Running

Populate a file in the same directory as `cnameshovel.py` named `url.txt`.  One URL per line, including the `http://` or `https://`

Run `python ./cnameshovel.py`

Results are in `results.txt`

Verbose stuff comes out of the console.  After a long run, look for timeouts from some pages in stdout.
