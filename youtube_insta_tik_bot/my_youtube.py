import pytube

def youtube_save(link): 
    yt = pytube.YouTube(link)
    stream = yt.streams.first()
    stream.download(filename = "video.mp4")
    return stream.get_file_path(filename="video.mp4")