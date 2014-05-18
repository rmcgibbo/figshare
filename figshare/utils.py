from six.moves.html_parser import HTMLParser

def strip_html(html):
    class MLStripper(HTMLParser):
        def __init__(self):
            self.reset()
            self.strict = False
            self.fed = []
        def handle_data(self, d):
            self.fed.append(d)
        def get_data(self):
            return ''.join(self.fed)
    p = MLStripper()
    p.feed(html)
    return p.get_data()