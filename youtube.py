from pytube import YouTube
import sys,os,pyperclip
path="" #--Path--


def sort_audio(s):
    temp=s[0].split("k")[0]
    return int(temp)
 
 
def sort_video(s):
    temp=s[0].split("p")[0]
    return int(temp)


def find_mx(mn):
    #print(mn)
    max_mp=mn[-1][0].split(" ")[0]
    max_val=len(mn)
    temp=1
    for i in mn:
       if str(max_mp) in i[0] and ("mp4" in i[0] or "mp3" in i[0]):
            max_val=temp
       temp=temp+1
    if "mp4" in sys.argv or "mp3" in sys.argv:
        max_val=len(mn)
        for i in range(1,len(mn)+1):
            if "mp4" in mn[i-1][0] or "mp3" in mn[i-1][0]:
                max_val=i
    #print(max_val)
    return max_val
            

def audio_download(yt,video=0):
    mn=[];ch=0
    for i in yt.streams.filter(type="audio"):
        #print(i)
        b_rate=ext="";temp=[]
        for y in str(i).split(" "):
            if "abr" in y:
                b_rate=str(y.split("=")[-1].replace('"',""))
            if "mime_type" in y:
                ext=str(y.split("=")[-1].replace('"',"").split("/")[-1]) 
        temp.append(b_rate+" "+ext)
        temp.append(ch)
        mn.append(temp)
        ch=ch+1
    mn.sort(key=sort_audio);ch=1
    if video==0 and "max" not in sys.argv or True:
        for i in mn:
            print(str(ch)+"."+str(i[0]))
            ch=ch+1
    choose=0
    if video==1 or "mp3" in sys.argv or "mp4" in sys.argv:
        choose=find_mx(mn)
        print(f"Enter :{choose}")
    while( 1 > choose or choose > len(mn)):
        choose=input("Enter :")
        try:
            choose=int(choose)
        except:
            quit()
    yt.streams.filter(type='audio')[mn[choose-1][1]].download(path)
    if(choose==3):
        file='"'+path+yt.title
        try:
            command=f'rename "{path}{yt.title}.mp4" "{yt.title}.mp3"'
            os.system("rename "+'"'+path+yt.title+'.mp4" '+'"'+yt.title+ '.mp3" >nul 2>&1')
        except:
            pass


def download(link):
    try:
        yt=YouTube(link)
    except:
        print("Connection Error")
        quit()
    audio=-1
    for i in sys.argv:
        if "audio=" in i:
            audio=i.split("=")[-1]
            break
    if audio==-1:
        audio=input("Audio :")
    try:
        audio=int(audio)
    except:
        quit()
    if(audio==1):
       audio_download(yt)
    elif audio!=1 or audio!=0:
        quit()
    elif audio==0:
        mn=[];ch=0
        video_pr=yt.streams.filter(type="video")
        if "pro" in sys.argv:
            video_pr=yt.streams.filter(type="video").filter(progressive="true")
        for i in video_pr:
            #print(i)
            res=ext="";temp=[]
            for y in str(i).split(" "):
                if "res=" in y:
                    res=str(y.split("=")[-1].replace('"',""))
                if "mime_type" in y:
                    ext=str(y.split("=")[-1].replace('"',"").split("/")[-1])
            temp.append(res+" "+ext)
            temp.append(ch)
            mn.append(temp)
            ch=ch+1
        mn.sort(key=sort_video);ch=1
        if "test" not in sys.argv:
                for i in mn:
                    print(str(ch)+"."+str(i[0]))
                    ch=ch+1
        choose=0
        if "max" in sys.argv:
            choose=find_mx(mn)
        while( 1 > choose or choose > len(mn)):
            choose=input("Enter :")
            try:
                choose=int(choose)
            except:
                quit()
        yt.streams.filter(type='video')[mn[choose-1][1]].download(path)
        if "pro" not in sys.argv:
            audio_download(yt,1)
    print("Done")



def main():
    link_list=[]
    start_check=True
    clip_check=False
    if "clip" in sys.argv:
        clip_check=True
    if "do" in sys.argv:
        sys.argv.append("audio=1")
        sys.argv.append("mp3")
    while True:
        link='';loop_break=0
        for i in sys.argv:
            if "link" in i:
                link=i.split("link=")[-1]
                loop_break=1
                break
        if "test" not in sys.argv and link=='' and "clip" not in sys.argv:
            link=input("Enter Link :")
        elif "test" in sys.argv:
            link="https://www.youtube.com/watch?v=6EEW-9NDM5k"
            loop_break=1
        elif clip_check:
            if pyperclip.paste() not in link_list:
                link=pyperclip.paste()
                link_list.append(link)
            else:
                link=''
            #print(link)
        if(link!=''):
            if "youtube" in link:
                download(link)
                link=""
                if start_check:
                    start_check=False
            else:
                if start_check:
                    pass
                else:
                    break
            if "loop" not in sys.argv or loop_break:
                quit()


if __name__=="__main__":
    main()