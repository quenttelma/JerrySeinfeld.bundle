TITLE = 'Jerry Seinfeld'
BASE_URL = 'http://www.jerryseinfeld.com'
RE_VIDEOS = Regex('data\("video", ([^\)]+?)\)')

###################################################################################################
def Start():

  ObjectContainer.title1 = TITLE
  HTTP.CacheTime = CACHE_1HOUR

###################################################################################################
@handler('/video/jerryseinfeld', TITLE)
def MainMenu():

  oc = ObjectContainer()
  page_content = HTTP.Request(BASE_URL).content

  for video in RE_VIDEOS.finditer(page_content):
    video_details = JSON.ObjectFromString(video.group(1))

    oc.add(CreateVideoClipObject(
      url = video_details['mp4'],
      title = video_details['title'],
      thumb = video_details['jpg']
    ))

  return oc

###################################################################################################
@route('/video/jerryseinfeld/createvideoclipobject')
def CreateVideoClipObject(url, title, thumb, include_container=False):

  videoclip_obj = VideoClipObject(
    key = Callback(CreateVideoClipObject, url=url, title=title, thumb=thumb, include_container=True),
    rating_key = url,
    title = title,
    thumb = thumb,
    items = [
      MediaObject(
        parts = [
          PartObject(key=url)
        ],
        container = Container.MP4,
        video_codec = VideoCodec.H264,
        video_resolution = 'sd',
        audio_codec = AudioCodec.AAC,
        audio_channels = 2,
        optimized_for_streaming = True
      )
    ]
  )

  if include_container:
    return ObjectContainer(objects=[videoclip_obj])
  else:
    return videoclip_obj
