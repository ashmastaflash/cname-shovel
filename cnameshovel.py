# Special thanks to http://pythonscraping.com/blog/javascript
# and http://daringfireball.net/2009/11/liberal_regex_for_matching_urls

from selenium import webdriver
from multiprocessing.dummy import Pool as ThreadPool
import dns.resolver
import os
import re
import signal
import time
from urlparse import urlparse


target_file_name = 'urls.txt'
max_threads = 10  # Number of parallel jobs to run

def get_page_source(url):
    print("Starting web driver for URL: %s" % url)
    driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
    driver.set_page_load_timeout(20)
    try:
        driver.get(url)
        time.sleep(5)
        source = str(driver.page_source.encode('unicode-escape'))
    except:
        print("Web driver timeout or exception on page %s" % url)
        source = ""
    print("Killing web driver for URL: %s" % url)
    driver.service.process.send_signal(signal.SIGTERM)
    driver.quit()
    print("Killed web driver for URL: %s" % url)
    return source

def get_urls_from_file(file_name):
    retlist = []
    with open(file_name, 'r') as in_file:
        contents = in_file.readlines()
    for target in contents:
        clean_target = target.rstrip('\n')
        if is_a_valid_url(clean_target):
            retlist.append(clean_target)
    return retlist

def get_urls_from_page_source(page_source):
    all_urls = []
    rx = r'\b((https*://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))'
    for match in re.finditer(rx, page_source):
        if is_a_valid_url(match.group(0)):
            all_urls.append(match.group(0))
    return all_urls

def is_a_valid_url(url):
    valid = True
    try:
        result = urlparse(url)
        if result.scheme not in ["http", "https"]:
            valid = False
        if not result.hostname:
            valid = False
    except Exception as e:
        print "\tEXC %s thrown for URL %s" % (e, url)
        valid = False
    return valid

def process_top_url(url):
    source = get_page_source(url)
    extracted_urls = get_urls_from_page_source(source)
    analyzed_targets = []
    print("Examining the source of %s shows these URLs: %s" % (url, str(extracted_urls)))
    for target in extracted_urls:
        print("Processing this URL now: %s" % target)
        parsed_target = urlparse(target)
        hostname = parsed_target.hostname
        if hostname is not None:
            derived_cnames = get_cname_path(hostname)
            analyzed_targets.append((hostname, derived_cnames))
        print("Done processing %s" % target)
    return (url, analyzed_targets)

def get_cname_path(hostname):
    in_list = [hostname]
    out_list = []
    print("Determining CNAME path for %s" % hostname)
    while len(in_list) > 0:
        print("\tIN LIST: %s" % str(in_list))
        print("\tOUT LIST: %s" % str(out_list))
        try:
            target_hostname = in_list.pop()
            out_list.append(target_hostname)
            result = dns.resolver.query(target_hostname, 'CNAME')
            for res in result:
                print("\tDNS resolver result for %s... %s" % (target_hostname, res))
                if res not in out_list:
                    print("\tAdding %s to out_list" % res)
                    out_list.append(str(res))
        except Exception as e:
            print("\tException %s in get_cname_path for %s" % (e, hostname))
            pass
    print("Finished CNAME path for %s" % hostname)
    return out_list

def main():
    here_dir = os.path.dirname(os.path.abspath(__file__))
    full_target_path = os.path.join(here_dir, target_file_name)
    outfile_path = os.path.join(here_dir, 'results.txt')
    url_list = get_urls_from_file(full_target_path)
    pool = ThreadPool(max_threads)
    results = pool.map(process_top_url, url_list)
    pool.close()
    pool.join()
    for url in url_list:
        results.append(process_top_url(url))
    with open(outfile_path, 'w') as out_file:
        for t in results:
            fmt = "\nBase: %s\n" % t[0]
            for u in t[1]:
                fmt += "\tDetected: %s\n" % u[0]
                for v in u[1]:
                    fmt += "\t\trecursive CNAME: %s\n" % v.encode('unicode-escape')
            out_file.write(fmt)

if __name__ == "__main__":
    main()
