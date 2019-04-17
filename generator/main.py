import os
import re
import urllib.parse
import firebase_admin
from firebase_admin import credentials, storage
from category import Category
from actor import Actor
from sound import Sound


cred = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(cred, { 'storageBucket': 'everyone-has-problems.appspot.com' })
bucket = storage.bucket()


def find_all_local_files(root='../sounds', files={}):

    for file_or_folder in os.listdir(root):

        complete_path = "{}/{}".format(root, file_or_folder)

        if complete_path.endswith('.mp3') or complete_path.endswith('.png'):
            files[complete_path.replace('../', '')] = complete_path
        elif os.path.isdir(complete_path):
            find_all_local_files(complete_path)

    return files


def find_all_storage_files():

    files = {}

    for blob in bucket.list_blobs():
        if blob.name.endswith('.mp3') or blob.name.endswith('.png'):
            public_url = "https://firebasestorage.googleapis.com/v0/b/everyone-has-problems.appspot.com/o/{}?alt=media"\
                .format(urllib.parse.quote_plus(blob.name))
            files[blob.name] = public_url

    return files


def upload_missing_files(local_files_dict:dict, storage_files_list:dict):

    print("Syncing files:")

    total = len(local_files_dict)
    total_added = 0
    total_removed = 0

    for storage_file, _ in storage_files_list.items():
        if storage_file in local_files_dict:
            del local_files_dict[storage_file]
            print(" [ ] skipped {}".format(storage_file))
        else:
            blob = bucket.blob(storage_file)
            blob.delete()
            print(" [-] removed {}".format(storage_file))
            total_removed += 1

    for storage_file_name, local_file_name in local_files_dict.items():
        print(" [+] uploading {}".format(storage_file_name))
        blob = bucket.blob(storage_file_name)
        blob.upload_from_filename(local_file_name)
        total_added += 1

    print("\nSynced files:\n - {} local\n - {} storage\n - added {}\n - removed {}"
          .format(total, len(storage_files_list), total_added, total_removed))


def replace_main_list():

    categories = create_category_tree()

    templates = """
        <template id="home.html">
            <ons-page id="home">
                <ons-toolbar>
                    <div class="center">Everyone has problems...</div>
                </ons-toolbar>
                <ons-list id="main-list">
        """

    for _, category in categories.items():

        templates += """
            <ons-list-item modifier="chevron longdivider" tappable onclick="pushPage('{}.html')">
                <div class="left">
                    <img class="list-item__thumbnail" src="{}">
                </div>
                <div class="center">
                    <span class="list-item__title">{}</span>
                    <span class="list-item__subtitle"></span>
                </div>
            </ons-list-item>
            """.format(category.template_name, category.image_url, category.title)

    templates += """
                </ons-list>
            </ons-page>
        </template>
        """

    for _, category in categories.items():

        templates += """
            <template id="{}.html">
                <ons-page id="home">
                    <ons-toolbar>
                        <div class="left"><ons-back-button></ons-back-button></div>
                        <div class="center">{}</div>
                    </ons-toolbar>
                    <ons-list id="main-list">
            """.format(category.template_name, category.title)

        for _, actor in category.actors.items():

            templates += """
                <ons-list-item modifier="chevron longdivider" tappable onclick="pushPage('{}.html')">
                    <div class="left">
                        <img class="list-item__thumbnail" src="{}">
                    </div>
                    <div class="center">
                        <span class="list-item__title">{}</span>
                        <span class="list-item__subtitle"></span>
                    </div>
                </ons-list-item>
                """.format(actor.template_name, actor.image_url, actor.title)

        templates += """
                    </ons-list>
                </ons-page>
            </template>
            """

    for _, category in categories.items():
        for _, actor in category.actors.items():

            templates += """
                <template id="{}.html">
                    <ons-page id="home">
                        <ons-toolbar>
                            <div class="left"><ons-back-button></ons-back-button></div>
                            <div class="center">{}</div>
                        </ons-toolbar>
                        <ons-list id="main-list">
                """.format(actor.template_name, actor.title)

            for _, sound in actor.sounds.items():
                templates += """
                    <ons-list-item modifier="longdivider" tappable onclick="playSound('sound-{}', '{}')">
                        <div class="left">
                            <img id="sound-{}" class="list-item__thumbnail" src="/static/img/play.png">
                        </div>
                        <div class="center">
                            <span class="list-item__title">{}</span>
                            <span class="list-item__subtitle"></span>
                        </div>
                    </ons-list-item>
                    """.format(sound.template_name, sound.mp3_url, sound.template_name, sound.title)

            templates += """
                        </ons-list>
                    </ons-page>
                </template>
                """


    with open('../public/index.html') as f:
        html = re.sub(r'<!--\s*TEMPLATES_START\s*-->[\s\S]*?<!--\s*TEMPLATES_END\s*-->',
                      "<!-- TEMPLATES_START -->{}<!-- TEMPLATES_END -->".format(templates),
                      f.read())

    with open('../public/index.html', 'w') as f:
        f.write(html)


def create_category_tree():

    categories = {}

    # First find all categories
    for remote_name, remote_url in storage_files.items():
        if re.match(r'^sounds/[^/]+/image.png$', remote_name):
            category = Category(remote_name, remote_url)
            categories[category.short_name] = category

    # Then find all actors in eacht category
    for remote_name, remote_url in storage_files.items():
        if re.match(r'^sounds/[^/]+/[^/]+/image.png$', remote_name):
            actor = Actor(remote_name, remote_url)
            categories[actor.category_name].actors[actor.short_name] = actor

    # And finally find all sounds for each actor
    for remote_name, remote_url in storage_files.items():
        if re.match(r'^sounds/[^/]+/[^/]+/.+.mp3$', remote_name):
            sound = Sound(remote_name, remote_url)
            categories[sound.category_name].actors[sound.actor_name].sounds[sound.short_name] = sound

    return categories


local_files = find_all_local_files()
storage_files = find_all_storage_files()

upload_missing_files(local_files, storage_files)
replace_main_list()
