import json
import os
import sys
from translate import Trans
dir = os.path.dirname(
            os.path.realpath(__file__))

def return_server(id, lang="en_US"):
    return {'id': int(id),
            'resistricted': False,
            'language': lang}


def server_save(server: dict):
    with open(dir + '/servers/%s.json' % server['id'], 'w') as w:
        json.dump(server, w)


def server_load(id):
    with open(dir + '/servers/%s.json' % id, 'r') as r:
        return json.load(r)


def server_init(bot):
    for server in list(bot.servers):
        id = server.id
        if os.path.exists('servers/%s.json' % id):
            pass
        else:
            server_save(return_server(id))


class Serverlist():
    def __init__(self):
        self.list = {}
        self.trans = Trans()
        for filename in os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/servers'):
            if '.json' in filename:
                with open(os.path.dirname(os.path.realpath(__file__)) + '/servers/%s' % filename, 'r') as r:
                    jsonfile = json.load(r)
                    self.list[int(jsonfile['id'])] = jsonfile

    def reload(self):
        self.list = {}
        for filename in os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/servers'):
            if '.json' in filename:
                with open(os.path.dirname(os.path.realpath(__file__)) + '/servers/%s' % filename, 'r') as r:
                    jsonfile = json.load(r)
                    self.list[int(jsonfile['id'])] = jsonfile

    def setlang(self, id, lang):
        serverdict = self.list.get(int(id))
        serverdict['language'] = lang
        self.list[int(id)] = serverdict

    def append(self, server: dict):
        server_save(server)
        self.list[server['id']] = server

    def get(self):
        return self.list

    def ban(self, id):
        serverdict = self.list.get(int(id))
        serverdict['resistricted'] = True
        self.list[int(id)] = serverdict

    def unban(self, id):
        serverdict = self.list.get(int(id))
        serverdict['resistricted'] = False
        self.list[int(id)] = serverdict


serverlist = Serverlist()
