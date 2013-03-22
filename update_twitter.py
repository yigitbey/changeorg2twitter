from hammock import Hammock as ChangeOrg
from twitter import Twitter, OAuth

changeorg_api_key = ''
changeorg_secret = ''

twitter_oauth_token = ''
twitter_oauth_secret = ''

twitter_consumer_key = ''
twitter_consumer_secret = ''

twitter_message_template = "%s people signed the campaign today. Sign here now: %s"

#Full URL of the campaign
petition_url = ''


def get_petition_id(api_key,url):
    changeorg = ChangeOrg('https://api.change.org/v1')
    params = {
        'api_key': api_key,
        'petition_url':url,
    } 
    
    petition_id = changeorg.petitions.get_id.GET(params=params).json

    return petition_id.get('petition_id')
    
def get_signature_count(api_key,petition_id):
    changeorg = ChangeOrg('https://api.change.org/v1')

    params = {
        'api_key': api_key,
    } 

    petitions = changeorg.petitions(petition_id).signatures.GET(params=params).json
    signature_count = petitions.get('signature_count')

    return signature_count

def write_to_file(file_name,value): 
    with open(file_name, 'w+') as write_file:
        write_file.write(str(value)+'\n')

def read_from_file(file_name):
    with open(file_name) as f:
            content = f.read()

    return content
            

def post_to_twitter(message,oauth_token,oauth_secret,consumer_key,consumer_secret):
    t = Twitter(
        auth = OAuth(oauth_token,
                     oauth_secret,
                     consumer_key,
                     consumer_secret)
    )
    
    t.statuses.update(status=message)


if __name__=="__main__":
    petition_id = get_petition_id(changeorg_api_key, petition_url)
    signature_count = get_signature_count(changeorg_api_key, petition_id)
    last_count = int(read_from_file('last_count'))
    write_to_file('last_count',signature_count)
    change = signature_count - last_count

    twitter_message = twitter_message_template % (change,petition_url)
    post_to_twitter(twitter_message,
                    twitter_oauth_token,
                    twitter_oauth_secret,
                    twitter_consumer_key,
                    twitter_consumer_secret)


