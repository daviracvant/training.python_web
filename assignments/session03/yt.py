__author__ = 'rithychhen'

#import the YoutubeAPI class.
from youtube import Youtube

#function to list the region that I am interesting in.
def generate_supported_region_ids():
    regions_ids = {'Argentina': 'AR', 'Australia': 'AU', 'Brazil': 'BR', 'Canada': 'CA',
                   'Egypt': 'EG', 'France': 'FR', 'Germany': 'DE', 'Great Britain': 'GB',
                   'Hong Kong': 'HK', 'India': 'IN', 'Ireland': 'IE', 'Italy': 'IT',
                   'Japan': 'JP', 'Malaysia': 'MY', 'Mexico': 'MX', 'Netherlands': 'NL',
                   'New Zealand': 'NZ', 'Russia': 'RU', 'Saudi Arabia': 'SA', 'Singapore': 'SG',
                   'South Africa': 'ZA', 'South Korea': 'KR', 'Spain': 'ES', 'Sweden': 'SE',
                   'Switzerland': 'CH', 'Taiwan': 'TW', 'United States': 'US'}
    return regions_ids

#main
if __name__ == '__main__':
    #instantiate the youtubapi class. This would default the region to US and api string.
    youtube = Youtube()
    #get a dictionary of regions ids.
    regions_ids = generate_supported_region_ids()
    #a list to store the result.
    result = []
    #go through all regions ids.
    for name, region_id in regions_ids.iteritems():

        temp_result = dict()
        #first set the region to region id.
        youtube.set_region_id(region_id)
        #then do an api to youtube to get the top 10.
        status, body = youtube.get_most_popular_by_region()
        #if response from youtube is not okay then store the error.
        if status != 200:
            temp_result[name] = 'Unable to get data for %s' % name
        else:
            #okay response. parse youtube content and store to the list.
            temp_result[name] = youtube.parse_content(body)
        #finally add the dictionary to the list.
        result.append(temp_result)
    #lastly write the list to html file.
    youtube.write_to_html(result)
