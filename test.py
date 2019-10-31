"""
Balabit - devops test v0.9.2
Balazs Polya - pp-bp@bnet.hu
31-10-2019
requirements: Python 3.7 + feedparser module

functional deficiencies:
- work with UTF-8 encoded input
- relative links not works (base url/hostname not detectable from stdin)

"""
import sys
import re
import json
import logging
logging.basicConfig(level=logging.WARNING, format='%(message)s', )
# logging.basicConfig(level=logging.DEBUG, format='%(message)s', )
try:
    import feedparser
    feedparser_imported = True
except Exception as e:
    logging.error("feedparser not found, try: pip3 install feedparser")
    logging.error(e)
    exit(1)


def tests():
    assert (2 * 2 != "néha öt")
    assert (get_links('+2sAl<a .u3 href="https://linklink" "|&\'# > </a>2f') ==
            ['https://linklink'])
    assert ("atom" == feed_type("https://gist.githubusercontent.com/ToddG/1974656/raw/d2d2fd1f7c01b43a67b1c5f39694d9ab5e00903f/sample-atom-1.0-feed.xml"))
    assert ("rss" == feed_type("https://hup.hu/node/feed"))


def get_links(html_str: str):
    """
    search all <a> and <link> tags in html_str (must be a valid html input), and extract the url value from href attrib
    create a list with all matching tag and the urls of the these tags
    :return: list of tuples: (whole tag, url)
    """
    # todo work only absolute links (we got the html from std input -> the base url is unknown
    regex = "<(?:a|link)>?.* href=\"(https?:[^\"]*)\".*<?\/(?:a|link)?>"
    urls = list()
    try:
        matches = re.finditer(regex, html_str, re.MULTILINE)
    except ValueError:
        logging.error("regexp match error")
        exit(1)
        return False
    for match in matches:
        if len(match.groups()) != 1:
            logging.error("bad tag:", match.group())
            exit(1)
        match.group()
        urls.append(match.group(1))
    return urls


def check_links(urls):
    rss_feeds = list()
    atom_feeds = list()
    for url in urls:
        feed_class = feed_type(url)
        logging.debug("feedtyp:({0}), url: {1}".format(feed_class, url))
        if feed_class == "rss":
            rss_feeds.append(url)
        if feed_class == "atom":
            atom_feeds.append(url)
    return rss_feeds, atom_feeds


def feed_type(url):
    """
    detect url's feed type
    """
    try:
        feed_fd = feedparser.parse(url)
        feed_typ = feed_fd.version
        if "rss" in feed_typ:
            return "rss"
        if "atom" in feed_typ:
            return "atom"
        return feed_typ
    except Exception as feedparser_error:
        logging.info("feedparserror {0}".format(feedparser_error))
        return False
    return "not feed"


def json_output(rss_list, atom_list):
    """
    generate json from url lists to stdout
    """
    feeds_json = {"atom": atom_list, "rss": rss_list}
    json.dump(feeds_json, sys.stdout, indent=4)


def main():
    html_doc = sys.stdin.read()
    html_links = get_links(html_doc)
    rss_feed_ids, atom_feed_ids = check_links(html_links)
    json_output(rss_feed_ids, atom_feed_ids)


tests()
if __name__ == "__main__":
    main()
