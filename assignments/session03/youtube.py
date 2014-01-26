__author__ = 'rithychhen'

import requests
import codecs
from bs4 import BeautifulSoup


#A youtube api call to do the api call and parsing the return cotent.
class Youtube:

    #constructing the Youtube API object, default region to US.
    def __init__(self, region_id='US'):
        self.region_id = region_id
        self.most_popular_api = 'http://gdata.youtube.com/feeds/api/standardfeeds/%s/most_popular?v=2&max-results=11'

    #a simple function to set the regions.
    def set_region_id(self, region_id):
        self.region_id = region_id

    #a simple get request to youtube to get the most popular video by region.
    #using the request module to get a get request to youtube.
    #return value are status and content.
    def get_most_popular_by_region(self):
        api_string = self.most_popular_api % self.region_id
        response = requests.get(api_string)
        return response.status_code, response.content

    #parse the content from youtube using BeautifulSoup.
    def parse_content(self, content):
        parsed_content = []
        content = BeautifulSoup(content)
        content.prettify()
        for entry in content.find_all("entry"):
            parsed_content.append(self.gen_entry(entry))
        return parsed_content

    #generate a single video entry.
    def gen_entry(self, entry):
        entry_parsed = dict()
        title = entry.title.string
        video_id = entry.content.find("yt:videoid")
        link = "http://www.youtube.com/watch?v=%s" % video_id.string
        entry_parsed['title'] = "<a href='%s' target='_blank'>%s</a>" % (link, title)
        entry_parsed['duration'] = entry.content.find("yt:duration").get("seconds")
        author = entry.content.author.find('name')
        entry_parsed['Uploader'] = author.string
        entry_parsed['Published on'] = entry.published.string
        statistic = entry.content.find("yt:statistics")
        entry_parsed["View count"] = statistic.get("viewcount")
        #entry_parsed["avorite count"]= statistic.get("favoritecount")
        entry_parsed["Dislikes"] = statistic.get("numdislikes")
        entry_parsed["Likes"] = statistic.get("numlikes")
        return entry_parsed

    #write the result into html.
    def write_to_html(self, result):
        html = "<html><body><h2>Most popular videos by region</h2>"
        for item in result:
            #print item
            for name, content in item.iteritems():
                #print name
                html += "<h4>%s</h4>" % name
                if isinstance(content, str):
                    html += content + '<br/>'
                else:
                    html += "<ul>"
                    for sub_item in content:
                        temp_string = ''
                        for key, value in sub_item.iteritems():
                            if key == 'title':
                                html += "<li><b>%s</b>" % value
                            elif key == 'duration':
                                html += "<i style='margin-left: 25px'>%s seconds</i><br/>" % value
                            elif key == 'Dislikes' or key == "Likes":
                                continue
                            else:
                                temp_string += "%s : %s | " % (key, value)
                        html += temp_string + '</li>'
                    html += "</ul><br/>"
        html += "</body></html>"
        self.put_file(html)

    #write html to a file.
    def put_file(self, html):
        with codecs.open("most_popular.html", "w", "utf-8-sig") as f:
            f.write(html)
            f.close()

