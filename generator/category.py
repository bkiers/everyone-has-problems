import re


class Category:

    def __init__(self, name, image_url):
        self.id = name
        self.short_name = re.sub(r'^sounds/([^/]+)/image.png$', "\\1", name)
        self.template_name = "{}".format(self.short_name.replace('.', '-'))
        self.title = " ".join(["{}{}".format(str(s)[0].upper(), str(s)[1:])
                               for s in self.short_name.lower().split('.')])
        self.image_url = image_url
        self.actors = {}

    def __repr__(self):
        return "Category={{id={}, title={}, actors={}}}".format(self.id, self.title, self.actors)