import signal
import time
from selenium import webdriver


class Web(object):
    @classmethod
    def get_page_source(cls, url):
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
