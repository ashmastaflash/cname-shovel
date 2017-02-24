# Special thanks to http://pythonscraping.com/blog/javascript
# and http://daringfireball.net/2009/11/liberal_regex_for_matching_urls

from multiprocessing.dummy import Pool as ThreadPool
import os
from urlparse import urlparse
from shovel.utility import Utility
from shovel.web import Web
from shovel.dnslib import Dns


target_file_name = 'urls.txt'
max_threads = 10  # Number of parallel jobs to run


def process_top_url(url):
    source = Web.get_page_source(url)
    extracted_urls = Utility.get_urls_from_page_source(source)
    analyzed_targets = []
    print("Examining the source of %s shows these URLs: %s" % (url, str(extracted_urls)))
    for target in extracted_urls:
        print("Processing this URL now: %s" % target)
        parsed_target = urlparse(target)
        hostname = parsed_target.hostname
        if hostname is not None:
            derived_cnames = Dns.get_cname_path(hostname)
            analyzed_targets.append((hostname, derived_cnames))
        print("Done processing %s" % target)
    return (url, analyzed_targets)



def main():
    here_dir = os.path.dirname(os.path.abspath(__file__))
    full_target_path = os.path.join(here_dir, target_file_name)
    outfile_path = os.path.join(here_dir, 'results.txt')
    url_list = Utility.get_urls_from_file(full_target_path)
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
