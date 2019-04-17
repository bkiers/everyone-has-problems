import re


class Sound:

    def __init__(self, name, mp3_url):
        self.id = name
        self.category_name = re.sub(r'^sounds/([^/]+)/([^/]+)/(.+).mp3$', "\\1", name)
        self.actor_name = re.sub(r'^sounds/([^/]+)/([^/]+)/(.+).mp3$', "\\2", name)
        self.short_name = re.sub(r'^sounds/([^/]+)/([^/]+)/(.+).mp3$', "\\3", name)
        self.template_name = "{}-{}-{}".format(self.category_name.replace('.', '-'),
                                                    self.actor_name.replace('.', '-'),
                                                    self.short_name.replace('.', '-'))
        self.title = " ".join(["{}{}".format(str(s)[0].upper(), str(s)[1:])
                               for s in re.split(r'[.\-]', self.short_name.lower())])
        self.mp3_url = mp3_url

    def __repr__(self):
        return "Sound={{id={}, title={}, template_name={}}}".format(self.id, self.title, self.template_name)