# Author     Ziffixture (74087102)
# Date       11/20/2024 (MM/DD/YYYY)
# Version    1.0.0

# Scans the API dump for all members tagged "Service". Excludes services that are deprecated or marked "NotBrowsable".


from requests  import get
from json      import loads


API_DUMP_VERSION_URL  = "http://setup.roblox.com/versionQTStudio"
API_DUMP_URL          = "http://setup.roblox.com/{0}-API-Dump.json"


class ServiceRetrievalFailure(Exception): pass


def make_get_request(url):
    response = get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        raise ServiceRetrievalFailure()
        
def meets_required(tags):
    is_service = "Service" in tags
    is_relevant = "Deprecated" not in tags and "NotBrowsable" not in tags

    return is_service and is_relevant
        
def get_services():
    api_dump_version  = make_get_request(API_DUMP_VERSION_URL)
    api_dump          = loads(make_get_request(API_DUMP_URL.format(api_dump_version)))

    services = [
        class_member["Name"] 
        for class_member in api_dump["Classes"] 
        if (tags := class_member.get("Tags")) and meets_required(tags)
    ]
                    
    return ",\n".join(services), len(services)
    

if __name__ == "__main__":
    print(*get_services())
