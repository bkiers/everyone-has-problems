import re


class Actor:

    def __init__(self, name, image_url):
        self.id = name
        self.category_name = re.sub(r'^sounds/([^/]+)/([^/]+)/image.png$', "\\1", name)
        self.short_name = re.sub(r'^sounds/([^/]+)/([^/]+)/image.png$', "\\2", name)
        self.template_name = "{}-{}".format(self.category_name.replace('.', '-'),
                                                 self.short_name.replace('.', '-'))
        self.title = " ".join(["{}{}".format(str(s)[0].upper(), str(s)[1:])
                               for s in self.short_name.lower().split('.')])
        self.image_url = image_url
        self.sounds = {}

    def __repr__(self):
        return "Actor={{id={}, title={}, #sounds={}}}".format(self.id, self.title, len(self.sounds))