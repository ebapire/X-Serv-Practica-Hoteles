#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string


class myContentHandler(ContentHandler):

    def __init__ (self):
        self.hotel = {}
        self.hoteles = []
        self.flag = 0
        self.theContent = ""
        self.atrib = ""

    def normalize_whitespace(text):
        return string.join(string.split(text), ' ')

    def startElement(self, tag, attrs):
        if tag in ['name', 'phone', 'body', 'web', 'url', 'address', 'zipcode', 'latitude', 'longitude']:
            self.flag = 1
        elif tag == "item" and attrs["name"] in ["Categoria", "SubCategoria"]:
            self.atrib = attrs['name']
            self.flag = 1

    def endElement(self, tag):
        if tag in ['name', 'phone', 'body', 'web', 'address', 'zipcode', 'latitude', 'longitude']:
            self.hotel[tag] = self.theContent
        if tag == 'item':
            self.hotel[self.atrib] = self.theContent
            self.atrib = ""
        if tag == 'url':
            try:
                self.hotel[tag].append(self.theContent)
            except KeyError:
                self.hotel[tag] = [self.theContent]

        if tag == "service":
    	    self.hoteles.append(self.hotel)
    	    self.hotel = {}
        if self.flag:
            self.flag = 0
            self.theContent = ""

    def characters (self, chars):
        if self.flag:
            self.theContent = self.theContent + chars

    # RETURN ALL THE DATA
    def terminar (self):
        return (self.hoteles)
