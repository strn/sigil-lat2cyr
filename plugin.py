#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

from   datetime  import datetime
from   lxml      import etree
import lib.py2srbcyr as pycir

# Global variables
MODNAME = 'Lat2Cyr'
# HTML tags that can contain text requireing transliteration
HTML_TAGS = ('a', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'p', 'br', 'b', 'i', 'em', 'span', 'sub', 'sup', 'title', 'th', 'td', 'li', 'strong', 'u')
GLOBAL_HTML4_ATTRS = ('accesskey', 'class', 'dir', 'id', 'lang', 'style', 'tabindex', 'title',)
# Dictionary that specifies which attributes are supported by which HTML tags
ALLOWED_ATTRIBS = {
	'br' : GLOBAL_HTML4_ATTRS,
	'body' : GLOBAL_HTML4_ATTRS,
	'table' : ('align', 'bgcolor', 'border', 'cellpadding', 'cellspacing', 'frame', 'rules', 'sortable', 'summary', 'width',),
	'td' : ('abbr', 'align', 'axis', 'bgcolor', 'char', 'charoff', 'colspan', 'headers', 'height', 'nowrap', 'rowspan', 'scope', 'valign', 'width',) + GLOBAL_HTML4_ATTRS,
	'tr' : ('align', 'bgcolor', 'char', 'charoff', 'valign',) + GLOBAL_HTML4_ATTRS,
	'img' : ('alt', 'class', 'ismap', 'src', 'style', 'width',) + GLOBAL_HTML4_ATTRS,
	'svg' : ('xmlns', 'xmlns:link', 'height', 'version', 'width',),
    'image' : ('xlink:href', 'height', 'width')
}
# Dictionary that says what attribute can be added to what tag, if missing
ADD_IF_MISSING_ATTRS = {
	'img' : ( ('alt', 'img'), )
}
# Special tags for eBook files
EBOOK_TAGS = ( 'text', 'creator', 'contributor', 'description', 'meta', 'publisher', 'subject', 'title' )
EBOOK_TAGS_ATTRIBUTES = { 'meta' : { 'name' : ('calibre:series', 'calibre:title_sort') } }
HTML_DOCTYPE = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
"""
NCX_DOCTYPE = """<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
   "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
"""


# Core function that converts text in HTML elements
# from Croatian Latin into Serbian Cyrillic script
def html_lat2cyr(tree, cyr, doctype):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    # Add META tag with correct encoding
    meta_el = tree.xpath("//meta[@charset or @content]")
    if not meta_el:
        # Add META tags that define content
        head_elem = tree.find('head')
        if head_elem is not None:
            metachr = etree.SubElement(head_elem, 'meta')
            metachr.set(u'http-equiv', u"content-type")
            metachr.set(u'content', u"text/html; charset=utf-8")
            metachr.text = ''

    # Walk over tree, changing text nodes
    for elem in tree.getiterator():
        if elem.tag in HTML_TAGS:
            if elem.text is not None:
                elem.text = cyr.text_to_cyrillic(elem.text)
            if elem.tail is not None:
                elem.tail = cyr.text_to_cyrillic(elem.tail)
        if elem.tag in ADD_IF_MISSING_ATTRS:
            for (attr, values) in ADD_IF_MISSING_ATTRS.items():
                for val in values:
                    if val[0] not in elem.attrib.keys():
                        # print(f"Element '{elem.tag}' is missing attribute {attr}")
                        elem.attrib[val[0]] = val[1]
        # Check if all attributes are in list of allowed/supported
        if elem.tag in ALLOWED_ATTRIBS.keys():
            for attr in elem.attrib.keys():
                if attr not in ALLOWED_ATTRIBS[elem.tag]:
                    del elem.attrib[attr]
        if elem.tag == 'html':
            # Replace existing 'lang' and 'xml:lang' attributes
            elem.attrib['lang'] = 'sr'
            elem.attrib['xml:lang'] = 'sr'
        elif elem.tag == 'svg' and 'xmlns:xlink' not in elem.attrib.keys():
            elem.attrib['xmlns:xlink'] = 'http://www.w3.org/1999/xlink'
    if not has_translit_comment(tree):
        tree.append(etree.Comment(f"Пресловљено програмом-додатком '{MODNAME}'; време: {ts}"))
    return etree.tostring(tree, pretty_print=True, xml_declaration=True,
        doctype=doctype, encoding='utf-8')


def has_translit_comment(tree):
    comments = tree.xpath('//comment()')
    for c in comments:
        if c.text.find(MODNAME) > -1:
            return True
    return False

# Core function that converts text in XML elements
# from Croatian Latin into Serbian Cyrillic script
def xml_lat2cyr(tree, cyr, doctype=None):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    # Walk over tree, changing text nodes
    for elem in tree.getiterator():
        # Remove namespace
        if not isinstance(elem.tag, str):
            continue
        leftbr = elem.tag.find('{')
        rightbr = elem.tag.find('}')
        if leftbr > -1 and rightbr > -1 and rightbr > leftbr:
            tag = elem.tag[rightbr+1:]
        else:
            tag = elem.tag

        if tag in EBOOK_TAGS:
            if elem.text is not None:
                elem.text = cyr.text_to_cyrillic(elem.text)
            # Convert some attributes
            if tag == 'meta' and 'name' in elem.attrib.keys():
                condList = EBOOK_TAGS_ATTRIBUTES['meta']['name']
                if elem.attrib['name'] in condList:
                    elem.attrib['content'] = cyr.text_to_cyrillic(elem.attrib['content'])
        elif tag == 'language':
            elem.text = 'sr'
    if not has_translit_comment(tree):
        tree.append(etree.Comment(f"Пресловљено програмом-додатком '{MODNAME}'; време {ts}"))
    return etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='utf-8', doctype=doctype)


def translit_toc(bk, xml_parser, cyr):
    # Transliterate ToC
    ncx_id = bk.gettocid()
    source = bk.readfile(ncx_id)
    tree = etree.XML(source.encode('utf-8'), xml_parser)
    transliterated = xml_lat2cyr(tree, cyr, NCX_DOCTYPE)
    bk.writefile(ncx_id, transliterated)
    print(f"Пресловљен садржај књиге")


def translit_metadata(bk, xml_parser, cyr):
    source = bk.getmetadataxml()
    tree = etree.XML(source.encode('utf-8'), xml_parser)
    transliterated = xml_lat2cyr(tree, cyr)
    bk.setmetadataxml(transliterated)
    print(f"Пресловљени метаподаци у датотеци 'content.opf'")


def translit_pages(bk, html_parser, cyr):
    for (id, href,) in bk.text_iter():
        # Ugly hack to preserve &nbsp; in HTML file
        # after encoding to UTF-8 for parser
        source = bk.readfile(id).replace('&nbsp;', '&#9208;')
        tree = etree.HTML(source.encode('utf-8'), html_parser)
        transliterated = html_lat2cyr(tree, cyr, HTML_DOCTYPE)
        bk.writefile(id, transliterated)
        print(f"Пресловљена датотека '{href}'")


def run(bk):
    cyr = pycir.SerbCyr()
    html_parser = etree.HTMLParser(remove_blank_text=True, remove_comments=False, encoding='utf-8')
    xml_parser = etree.XMLParser(remove_blank_text=True, remove_comments=False, encoding='utf-8')

    print("Пресловљавање ЕПУБ-а на српску ћирилицу...")
    translit_toc(bk, xml_parser, cyr)
    translit_metadata(bk, xml_parser, cyr)
    translit_pages(bk, html_parser, cyr)
    print("Завршено - не заборавите да 'ручно' замените: '⏸' са '&\u200Cnbsp;' у целом ЕПУБ-у!")
    return 0


def main():
    print("Долазак у ову функцију није требало да се деси.\n")
    return -1


if __name__ == "__main__":
    exit(main())
