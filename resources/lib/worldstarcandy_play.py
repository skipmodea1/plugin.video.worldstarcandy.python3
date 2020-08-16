#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
# Imports
#
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
from worldstarcandy_const import ADDON, SETTINGS, LANGUAGE, DATE, VERSION, HEADERS, convertToUnicodeString, log, getSoup
import requests
import sys
import urllib.parse
import xbmc
import xbmcgui
import xbmcplugin


#
# Main class
#
class Main(object):
    #
    # Init
    #
    def __init__(self):
        # Get the command line arguments
        # Get the plugin url in plugin:// notation
        self.plugin_url = sys.argv[0]
        # Get the plugin handle as an integer number
        self.plugin_handle = int(sys.argv[1])

        # Get plugin settings
        self.VIDEO = SETTINGS.getSetting('video')

        log("ARGV", repr(sys.argv))

        # Parse parameters...
        self.video_page_url = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['video_page_url'][0]
        # Get the title.
        self.title = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)['title'][0]
        self.title = str(self.title)

        log("self.video_page_url", self.video_page_url)

        #
        # Play video...
        #
        self.playVideo()

    #
    # Play video...
    #
    def playVideo(self):
        #
        # Init
        #
        is_folder = False
        # Create a list for our items.
        listing = []
        unplayable_media_file = False
        have_valid_url = False
        dialogWait = xbmcgui.DialogProgress()

        #
        # Get current list item details...
        #
        # title = xbmc.getInfoLabel("listitem.Title")
        thumbnail_url = xbmc.getInfoImage("list_item.Thumb")
        # studio = xbmc.getInfoLabel("list_item.Studio")
        plot = xbmc.getInfoLabel("list_item.Plot")
        genre = xbmc.getInfoLabel("list_item.Genre")

        #
        # Get HTML page
        #
        response = requests.get(self.video_page_url, headers=HEADERS)

        html_source = response.text
        html_source = convertToUnicodeString(html_source)

        #log ("html_source1", html_source)

        begin_pos_video_file = str(html_source).find("http://www.worldstarhiphop.com/embed/")
        end_pos_video_file = str(html_source).find('&quot;', begin_pos_video_file)
        video_url = html_source[begin_pos_video_file:end_pos_video_file]

        log("video_url1", video_url)

        try:
            #
            # Get HTML page
            #
            response = requests.get(video_url, headers=HEADERS)

            html_source = response.text
            html_source = convertToUnicodeString(html_source)

            #log ("html_source2", html_source)

            # It should contain something like this:
            # <source src="http://hw-videos.worldstarhiphop.com/u/vid/2015/03/15/Sequencealeganfgilswetseassisndede1.flv" type="video/mp4">
            pos_vid_url = str(html_source).find("hw-videos.worldstarhiphop.com/")
            if pos_vid_url >= 0:
                pos_start_quote = str(html_source).rfind('"', 0, pos_vid_url)
                pos_end_quote = str(html_source).find('"', pos_start_quote + 1)
                video_url = html_source[pos_start_quote + 1: pos_end_quote]
                have_valid_url = True
            else:
                unplayable_media_file = True
        except:
            unplayable_media_file = True

        log("have_valid_url", have_valid_url)

        log("video_url2", video_url)

        if have_valid_url:
            list_item = xbmcgui.ListItem(path=video_url)
            xbmcplugin.setResolvedUrl(self.plugin_handle, True, list_item)
        #
        # Alert user
        #
        elif unplayable_media_file:
            xbmcgui.Dialog().ok(LANGUAGE(30000), LANGUAGE(30506))