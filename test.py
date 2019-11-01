"""
Balabit - devops test v0.9.3
pp-bp@bnet.hu
31-10-2019
requirements:
    - Python 3.7
    - feedparser module
functional deficiencies:
    - relative links not works (base url/hostname not detectable from stdin)
"""
import re
import sys
import json
import logging
import threading
# logging.basicConfig(level=logging.WARNING, format='%(message)s', )
logging.basicConfig(level=logging.DEBUG, format='%(message)s', )
try:
    import feedparser
except Exception as e:
    logging.error("feedparser not found, try: pip3 install feedparser - {0}".format(e))
    exit(1)


def tests():
    assert (2 * 2 != "néha öt")
    assert (get_links('+2sAl<a .u3 href="https://linklink" "|&\'# > </a>2f') ==
            ['https://linklink'])
    assert ("atom" == feed_type("https://gist.githubusercontent.com/ToddG/1974656/raw/"
                                "d2d2fd1f7c01b43a67b1c5f39694d9ab5e00903f/sample-atom-1.0-feed.xml"))
    assert ("rss" == feed_type("http://static.userland.com/gems/backend/rssTwoExample2.xml"))
    assert ("rss" == feed_type("http://static.userland.com/gems/backend/gratefulDead.xml"))
    assert ("rss" == feed_type("http://static.userland.com/gems/backend/sampleRss.xml"))


def get_links(html_str: str):
    """
    search all <a> and <link> tags (must be a valid html input), and extract the url value from href attrib
    :return: list of urls
    """
    regex = '<(?:a|link)>?.* href=\"(https?:[^\"]*)\".*<?\/(?:a|link)?>'
    urls = list()
    try:
        matches = re.finditer(regex, html_str, re.MULTILINE)
        for match in matches:
            if len(match.groups()) != 1:
                logging.error("bad tag:", match.group())
                exit(1)
            match.group()
            urls.append(match.group(1))
        logging.debug(("total url found: {0}".format(len(urls))))
    except ValueError:
        logging.error("regexp match error")
        exit(1)
    return urls


def thread_fn(tid, url):
    feed_class = feed_type(url)
    if feed_class == "rss":
        rss_feed_list.append(url)
    if feed_class == "atom":
        atom_feed_list.append(url)
    logging.debug("thread: {0} finished (feed_class: {1}, url: {2})".format(tid, feed_class, url))


def check_links(urls):
    threads = list()
    for th_id, url in enumerate(urls):
        th = threading.Thread(target=thread_fn, args=(th_id, url, ))
        th.start()
        threads.append(th)
    for thread in threads:
        thread.join()
    return True


def feed_type(url):
    """
    detect url's feed type (if feed)
    """
    try:
        feed_fd = feedparser.parse(url)
        feed_typ = feed_fd.version
        if "rss" in feed_typ:
            return "rss"
        if "atom" in feed_typ:
            return "atom"
        return "no feed"
    except Exception as feedparser_error:
        logging.debug("feedparserror {0}".format(feedparser_error))
        return False


def json_output(rss_list, atom_list):
    """
    generate json from url lists to stdout
    """
    feeds_json = {"atom": atom_list, "rss": rss_list}
    json.dump(feeds_json, sys.stdout, indent=4)


def main():
    global rss_feed_list, atom_feed_list
    rss_feed_list = list()
    atom_feed_list = list()
    try:
        html_doc = sys.stdin.read()
    except Exception as err:
        logging.error("can't read the stdin - {0}".format(err))
        exit(1)
    html_links = get_links(html_doc)
    check_links(html_links)
    json_output(rss_feed_list, atom_feed_list)


if logging.root.level < 30:
    tests()
if __name__ == "__main__":
    main()
