from googleapiclient.discovery import build
import pandas as panda
import os
import googleapiclient.discovery
from urllib.parse import urlparse, parse_qs


def main(video_id):

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv('DEVELOPER_KEY')

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

    # youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "")
    
    
    request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,   
        
        )
    response = request.execute()
    data = []
 
    while response:
            for item in response["items"]:
                item_info = item["snippet"]
                topLevelComment = item_info["topLevelComment"]
                comment_info = topLevelComment["snippet"]
                data.append({'comment_text': comment_info["textDisplay"]})   


            if 'nextPageToken' in response:
                    response = youtube.commentThreads().list(
                        part = 'snippet,replies',
                        videoId = video_id,
                        maxResults= 100,
                        pageToken=response['nextPageToken']  #get 100 comments
                    ).execute()
                    # data.append({'comment_text': comment_info["textDisplay"]})
            else:
                    break
                    
    print(data)        
    panda.DataFrame(data,columns=('comment_by', 'comment_text', 'comment_date', 'likes_count'))
    d_frame = panda.DataFrame(data)
    path = "Data/"+video_id+".csv"
    full_path = os.path.abspath(path)
    d_frame.to_csv(full_path)
    return full_path        







def parse_videoId(url):
    u_pars = urlparse(url)
    # ParseResult(scheme='https', netloc='www.youtube.com', path='/watch', params='', query='v=t1fZvTdEiFQ', fragment='')
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
    #    ['t1fZvTdEiFQ']
    # parse_qs stores data in an array so accessing it with index value
        return quer_v[0]
    
    pth = u_pars.path.split('/')
    if pth:
        print(pth[-1])
        return pth[-1]







if __name__ == "__main__":
    v_Id = parse_videoId("https://www.youtube.com/watch?v=t1fZvTdEiFQ")
    main(v_Id)
