import requests
import subprocess
import os
import pip
import re
import json
import urllib3
from contextlib import closing
urllib3.disable_warnings()

header_info={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    #'cookie': 'fts=1521024428; pgv_pvi=6015641600; im_notify_type_11743208=0; LIVE_BUVID=35570b9efe35b13b559a8f1e1111892c; LIVE_BUVID__ckMd5=b66ca168e960d1d0; buvid3=ABEFB80F-F5D5-47B4-A306-FA3283175637103054infoc; _ga=GA1.2.1195467944.1532734636; CURRENT_FNVAL=16; rpdid=|(J|~YRYm|~)0J\'ullYum)m)k; im_seqno_11743208=572; im_local_unread_11743208=0; _uuid=DA2F6410-5450-BC16-446C-7B6EC13F49B497214infoc; hasstrong=1; stardustvideo=1; laboratory=1-1; sid=5a25fr3x; CURRENT_QUALITY=116; bp_t_offset_11743208=383996649230477383; bsource=login_download_bili; DedeUserID=11743208; DedeUserID__ckMd5=b986b5754bc6a73e; SESSDATA=a60a3fbb%2C1603858919%2Cbefcf*51; bili_jct=dd226e39641d6e2908c4153c199be020; flash_player_gray=false; html5_player_gray=false; PVID=4',
    'Referer':"https://www.bilibili.com/",
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }

current_path = os.path.dirname(__file__)
videoCache=[]
if not os.path.exists(current_path+"/BilibiliDownload"):
      os.makedirs(current_path+"/BilibiliDownload")

if not os.path.exists(current_path+"/config.ini"):
    try:
        header_info={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'cookie': 'fts=1521024428; pgv_pvi=6015641600; im_notify_type_11743208=0; LIVE_BUVID=35570b9efe35b13b559a8f1e1111892c; LIVE_BUVID__ckMd5=b66ca168e960d1d0; buvid3=ABEFB80F-F5D5-47B4-A306-FA3283175637103054infoc; _ga=GA1.2.1195467944.1532734636; CURRENT_FNVAL=16; rpdid=|(J|~YRYm|~)0J\'ullYum)m)k; im_seqno_11743208=572; im_local_unread_11743208=0; _uuid=DA2F6410-5450-BC16-446C-7B6EC13F49B497214infoc; hasstrong=1; stardustvideo=1; laboratory=1-1; sid=5a25fr3x; CURRENT_QUALITY=116; bp_t_offset_11743208=383996649230477383; bsource=login_download_bili; DedeUserID=11743208; DedeUserID__ckMd5=b986b5754bc6a73e; SESSDATA=a60a3fbb%2C1603858919%2Cbefcf*51; bili_jct=dd226e39641d6e2908c4153c199be020; flash_player_gray=false; html5_player_gray=false; PVID=4',
            'Referer':"https://www.bilibili.com/",
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
            }
        data=json.dumps(header_info,sort_keys=True, indent=2)
        with open(current_path+"/config.ini", "w") as f:
            f.write(data)
    except Exception as e:
        print("配置文件写入错误："+str(e))

try:
    print('正在初始化 BDSIP (BiliBili Download System In Python)\n')
    with open(current_path+"/config.ini", "r") as f:
        header_info=eval(f.read())
        print("cookie :")
        print(header_info["cookie"])
        print()
        print("外部电源接触....没有异常")
except Exception as e:
    print("配置文件错误"+str(e))



current_path=current_path+"/BilibiliDownload"

class BilibiliDownloader:
    videoTitle=""  
    videoUrl=""
    ContentRange=0
    qn="116"
    audioUrl=""
    ContentRange_audio=0
    Bvid=""
    path=""
    LinkList=""
    #构造函数
    def __init__(self,bvid,qn="116"):        
         self.videoTitle=""
         self.videoUrl=""
         self.ContentRange=0
         self.qn=qn
         self.audioUrl=""
         self.ContentRange_audio=0
         self.Bvid=bvid
         self.path=""
         self.LinkList=""




    def getVideo_basicInfo(self):
        # header_info={
        #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #         'Accept-Encoding': 'gzip, deflate, br',
        #         'Accept-Language': 'zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
        #         'Cache-Control': 'max-age=0',
        #         'Connection': 'keep-alive',
        #         'Sec-Fetch-Dest': 'document',
        #         'cookie': 'fts=1521024428; pgv_pvi=6015641600; im_notify_type_11743208=0; LIVE_BUVID=35570b9efe35b13b559a8f1e1111892c; LIVE_BUVID__ckMd5=b66ca168e960d1d0; buvid3=ABEFB80F-F5D5-47B4-A306-FA3283175637103054infoc; _ga=GA1.2.1195467944.1532734636; CURRENT_FNVAL=16; rpdid=|(J|~YRYm|~)0J\'ullYum)m)k; im_seqno_11743208=572; im_local_unread_11743208=0; _uuid=DA2F6410-5450-BC16-446C-7B6EC13F49B497214infoc; hasstrong=1; stardustvideo=1; laboratory=1-1; sid=5a25fr3x; CURRENT_QUALITY=116; bp_t_offset_11743208=383996649230477383; bsource=login_download_bili; DedeUserID=11743208; DedeUserID__ckMd5=b986b5754bc6a73e; SESSDATA=a60a3fbb%2C1603858919%2Cbefcf*51; bili_jct=dd226e39641d6e2908c4153c199be020; flash_player_gray=false; html5_player_gray=false; PVID=4',
        #         'Referer':"https://www.bilibili.com/",
        #         'Sec-Fetch-Mode': 'cors',
        #         'Sec-Fetch-Site': 'same-origin',
        #         'Sec-Fetch-User': '?1',
        #         'Upgrade-Insecure-Requests': '1',
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        #         }
        try:

            if  "?"  in self.Bvid:
                print("尝试获取分P视频下载信息")
                url="https://api.bilibili.com/x/web-interface/view/detail?bvid="+self.Bvid.split("?")[0]+"&aid=&jsonp=jsonp"
            else:
                url="https://api.bilibili.com/x/web-interface/view/detail?bvid="+self.Bvid+"&aid=&jsonp=jsonp"
            request=requests.get(url=url,headers=header_info,allow_redirects=False)
            print("request.status_code"+str(request.status_code))
            kv=json.loads(request.text)
            kv=kv["data"]
            kv=kv["View"]

            regex = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]") # 匹配不是中文、大小写、数字、空格的其他字符
            self.videoTitle=string1 = regex.sub('', kv["title"]) #将string1中匹配到的字符替换成空字符
            if  "?"  in self.Bvid:
                self.videoTitle+="P"+self.Bvid[-1]
            if self.videoTitle=="":
                self.videoTitle=self.Bvid
            self.path=current_path+"/"+self.videoTitle+".mp4"
            print("视频：")
            print(self.videoTitle)
            #print(self.path)
        except Exception as e:
            print(str(e))
            print("错误")
        return



    def getVideoDownload_info(self):
        print("开始获取视频下载信息：\n")
        # header_info={
        #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #         'Accept-Encoding': 'gzip, deflate, br',
        #         'Accept-Language': 'zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
        #         'Cache-Control': 'max-age=0',
        #         'Connection': 'keep-alive',
        #         'Sec-Fetch-Dest': 'document',
        #         'cookie': 'fts=1521024428; pgv_pvi=6015641600; im_notify_type_11743208=0; LIVE_BUVID=35570b9efe35b13b559a8f1e1111892c; LIVE_BUVID__ckMd5=b66ca168e960d1d0; buvid3=ABEFB80F-F5D5-47B4-A306-FA3283175637103054infoc; _ga=GA1.2.1195467944.1532734636; CURRENT_FNVAL=16; rpdid=|(J|~YRYm|~)0J\'ullYum)m)k; im_seqno_11743208=572; im_local_unread_11743208=0; _uuid=DA2F6410-5450-BC16-446C-7B6EC13F49B497214infoc; hasstrong=1; stardustvideo=1; laboratory=1-1; sid=5a25fr3x; CURRENT_QUALITY=116; bp_t_offset_11743208=383996649230477383; bsource=login_download_bili; DedeUserID=11743208; DedeUserID__ckMd5=b986b5754bc6a73e; SESSDATA=a60a3fbb%2C1603858919%2Cbefcf*51; bili_jct=dd226e39641d6e2908c4153c199be020; flash_player_gray=false; html5_player_gray=false; PVID=4',
        #         'Referer':"https://www.bilibili.com/",
        #         'Sec-Fetch-Mode': 'cors',
        #         'Sec-Fetch-Site': 'same-origin',
        #         'Sec-Fetch-User': '?1',
        #         'Upgrade-Insecure-Requests': '1',
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        #         }
        url="https://www.bilibili.com/video/"+str(self.Bvid)

        try:

            request=requests.get(url=url,headers=header_info,allow_redirects=False)
            print("request.url"+request.request.url)
            print("Status : "+str(request.status_code))
            if request.status_code ==200:
                #if this video is Bangumi
                if "backup_url" not in request.text and "?" not in self.Bvid:
                    redirect_url="https://api.bilibili.com/x/web-interface/view/detail?bvid="+self.Bvid+"&aid=&jsonp=jsonp"
                    request.close()
                    print("需要重定向")
                    print("从"+redirect_url+"获取地址")
                    redirect=requests.get(url=redirect_url,headers=header_info,allow_redirects=False)

                    #print("redirect :\n"+redirect.text)
                    searchObj = re.search( r'("redirect_url":")(.*?)(","rights":{"bp")', redirect.text)
                    print("视频原始地址"+searchObj.group(2))
                    redirected_url=searchObj.group(2)
                    request=requests.get(url=redirected_url,headers=header_info,allow_redirects=False)


                    if "baseUrl" in request.text:
                        print("尝试获取Bangumi下载地址\n\n")
                        searchObj = re.search( r'(<script>window.__playinfo__=)(.*?)(</script>)', request.text)
                        kv=json.loads(searchObj.group(2))
                        
                        kv=kv["data"]["dash"]["video"]
                        kv=kv[0]
                        self.videoUrl = kv['baseUrl']
                        print("视频下载地址"+self.videoUrl)
                        kv=json.loads(searchObj.group(2))
                        kv=kv["data"]["dash"]["audio"]
                        kv=kv[0]
                        self.audioUrl=kv['baseUrl']
                        print("音频下载地址"+self.audioUrl)
                    else:
                        print("获取地址失败")

                #else this video is UGC
                else:
                    print("视频原始地址"+request.url+"\n")
                    print("尝试获取UGC下载地址\n\n")
                    # reg_video='(http://upos-sz)(.*?)(\', \')'
                    # #reg_audio='(http://upos-sz-mirrorkodo.bilivideo.com)(.*?)(\', \')'
                    # reg_audio='(http://upos-sz-mirrorhw)(.*?)(\', \')'
                    if  "?"  in self.Bvid:
                        print("尝试获取"+self.videoTitle+"下载地址")
                    if "baseUrl" in request.text:

                        searchObj = re.search( r'(<script>window.__playinfo__=)(.*?)(</script>)', request.text)
                        kv=json.loads(searchObj.group(2))
                        kv=kv["data"]["dash"]["video"]
                        kv=kv[0]
                        self.videoUrl = kv['baseUrl']
                        print("视频下载地址"+self.videoUrl)

                        print()

                        kv=json.loads(searchObj.group(2))
                        kv=kv["data"]["dash"]["audio"]
                        kv=kv[0]
                        self.audioUrl=kv['baseUrl']
                        print("音频下载地址"+self.audioUrl)

                    elif "Url" in request.text and "durl" in request.text:
                        print("此视频没有音频分离")
                        searchObj = re.search( r'(<script>window.__playinfo__=)(.*?)(</script>)', request.text)
                        kv=json.loads(searchObj.group(2))
                        self.LinkList=kv["data"]["durl"]
                        kv=kv["data"]["durl"][0]
                        self.videoUrl = kv["url"]
                        self.path=current_path+"/"+self.videoTitle
                        print("视频下载地址"+self.videoUrl)
                    else:
                        print("获取地址失败")
        except Exception as e:
            print(str(e))
            print("错误")
        return


    def getVideo_ContentRange(self):
        try:
            header={
                'accept': '*/*',
                'accept-encoding': 'identity',
                'accept-language': 'zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
                'if-range': '"5e9490bf-36d6fa"',
                'origin': 'https://www.bilibili.com',
                'range': 'bytes=2594126-2794294',
                'referer': 'https://www.bilibili.com/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
            }
            #获取视频Content-Range
            request=requests.get(url=self.videoUrl,headers=header, stream=True, verify=False)
            print("status_code :"+str(request.status_code))
            #print("Responseheaders :"+str(request.headers))
            kv=eval(str(request.headers))
            ContentRange=str(kv["Content-Range"])
            ContentRange=ContentRange.split('/')[1]
            self.ContentRange=ContentRange
            print("ContentRange :"+self.ContentRange)
            #获取音频Content-Range
            if self.audioUrl!="":
                request=requests.get(url=self.audioUrl,headers=header, stream=True, verify=False)
                print("status_code :"+str(request.status_code))
                #print("Responseheaders :"+str(request.headers))
                kv=eval(str(request.headers))
                ContentRange=str(kv["Content-Range"])
                ContentRange=ContentRange.split('/')[1]
                self.ContentRange_audio=ContentRange
                print("ContentRange_audio :"+self.ContentRange_audio)
        except Exception as e:
            print("错误")
            print(str(e))
    #开始下载视频

    def downloadVideo(self):
        Downloadheader={
        'Accept': '*/*',
        'Accept-Encoding': 'identity',
        'Accept-Language': 'zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Origin': 'https://www.bilibili.com',
        'Range': 'bytes=0-'+str(self.ContentRange),
        'Referer':"https://www.bilibili.com/"+self.Bvid,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        }
        try:
            print("开始下载视频")
            if self.LinkList=="":
                with closing(requests.get(url=self.videoUrl,headers=Downloadheader, stream=True, verify=False)) as response:
                    chunk_size = 102400  # 单次请求最大值
                    content_size = int(response.headers['content-length'])  # 内容体总大小
                    data_count = 0
                    with open(self.path, "wb") as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            data_count = data_count + len(data)
                            now_jd = (data_count / content_size) * 100
                            print("\r 文件下载进度：%d%%(%d/%d)" % (now_jd, data_count, content_size), end=" ")
            else:
                print("开始下载分段视频")

                part=0
                for link in self.LinkList:
                    self.videoUrl=link["url"]
                    self.getVideo_ContentRange()
                    Downloadheader={
                        'Accept': '*/*',
                        'Accept-Encoding': 'identity',
                        'Accept-Language': 'zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
                        'Connection': 'keep-alive',
                        'Origin': 'https://www.bilibili.com',
                        'Range': 'bytes=0-'+str(self.ContentRange),
                        'Referer':"https://www.bilibili.com/"+self.Bvid,
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'cross-site',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
                        }

                    with closing(requests.get(url=self.videoUrl,headers=Downloadheader, stream=True, verify=False)) as response:
                        chunk_size = 102400  # 单次请求最大值
                        content_size = int(response.headers['content-length'])  # 内容体总大小
                        data_count = 0
                        with open(self.path+"Part"+str(part)+".flv", "wb") as file:
                            for data in response.iter_content(chunk_size=chunk_size):
                                file.write(data)
                                data_count = data_count + len(data)
                                now_jd = (data_count / content_size) * 100
                                print("\r 文件下载进度：%d%%(%d/%d)-Part%d" % (now_jd, data_count, content_size,part), end=" ")
                    videoCache.append(self.path+"Part"+str(part)+".flv")
                    part+=1
                    




            # with open(self.path, "wb") as f:
            #     f.write(requests.get(url=self.videoUrl,headers=Downloadheader, stream=True, verify=False).content)
            print("下载完成")

        except Exception as e:
            print(str(e))
            print("错误")






    #开始下载音频

    def downloadAudio(self):
        Downloadheader_Audio={
                    'accept': '*/*',
                    'accept-encoding': 'identity',
                    'accept-language': 'zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
                    'if-range': '"5e9490bf-36d6fa"',
                    'origin': 'https://www.bilibili.com',
                    'range': 'bytes=2594126-2794294',
                    'referer': 'https://www.bilibili.com/',
                    'sec-fetch-dest': 'empty',
                    'Range': 'bytes=0-'+str(self.ContentRange_audio),
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'cross-site',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
                }
        try:
            print("开始下载音频")
            with open(self.path.split('.')[0]+"_audio.mp3", "wb") as f:
                f.write(requests.get(url=self.audioUrl,headers=Downloadheader_Audio, stream=True, verify=False).content)
            print("下载完成")
        except Exception as e:
            print(str(e))
            print("错误")






    def Convert(self):
        """
        视频添加音频
        :path: 传入视频文件的路径
        :path_Audio: 传入音频文件的路径
        :return:
        """
        
        current_path = os.path.dirname(__file__)
        print("开始合成")
        outfile_name = self.path.split('.')[0] + '_Converted.mp4'
        #outfile_name = "4月辉夜大小姐想让我告白 第二季正式PV" + '_Converted.mp4'
        print(outfile_name)
        subprocess.call(current_path+'/ffmpeg-20200501-39fb1e9-win64-static/bin/ffmpeg -i ' + self.path
                        + ' -i ' + self.path.split('.')[0]+"_audio.mp3" + ' -strict -2 -f mp4 '
                        + outfile_name, shell=True)
        print("已输出到"+str(self.path))






    def Convert_concat(self):
        """
        视频添加音频
        :path: 传入视频文件的路径
        :path_Audio: 传入音频文件的路径
        :return:
        """
        param=''
        current_path = os.path.dirname(__file__)
        current_path=current_path+"/BilibiliDownload"
        for item in videoCache:
            param+='file  '+'\''+item+'\''+"\n"
        PathoflistTxt=current_path+"/list.txt"
        PathoflistTxt=PathoflistTxt.replace("/","\\")

        with open(PathoflistTxt, "w") as f:
                f.write(param[:-1])
        current_path = os.path.dirname(__file__)
        print("开始合成")

        outfile_name = current_path+"/BilibiliDownload/"+self.videoTitle + '.flv'
        print(outfile_name)
        subprocess.call(current_path+'/ffmpeg-20200501-39fb1e9-win64-static/bin/ffmpeg -f ' + 'concat -safe 0 -i '+PathoflistTxt + ' -c copy '
                        + outfile_name, shell=True)
        print("已输出到"+str(self.path))


    def clean(self):
        print("正在清理下载缓存")
        try:
            if os.path.exists(self.path):  # 清理视频文件
                os.remove(self.path) 
            if os.path.exists(self.path.split('.')[0]+"_audio.mp3"):  # 清理音频文件
                os.remove(self.path.split('.')[0]+"_audio.mp3") 
            if os.path.exists(self.path.split('.')[0] + '_Converted.mp4'):  # 重命名
                os.rename(self.path.split('.')[0] + '_Converted.mp4',self.path.split('.')[0] + '.mp4') 
                print("清理成功")
        except Exception as e:
            print("清理失败"+str(e))



    def clean2(self):
        print("正在清理下载缓存")
        try:

            if len(videoCache)>1:
                for item in videoCache:
                    if os.path.exists(item):  # 清理视频缓存
                        os.remove(item)
                current_path = os.path.dirname(__file__)
                current_path=current_path+"/BilibiliDownload"
                PathoflistTxt=current_path+"/list.txt"
                if os.path.exists(PathoflistTxt):  # 临时数据
                        os.remove(PathoflistTxt) 
            print("清理成功")
        except Exception as e:
            print("清理失败"+str(e))






                          


def main():
    print("Please input Bvid")
    Bvid=input()
    #Bvid="BV12t4y127TD"
    Bd=BilibiliDownloader(Bvid)
    Bd.getVideo_basicInfo()
    Bd.getVideoDownload_info()
    if Bd.audioUrl!="":
        Bd.getVideo_ContentRange()
        Bd.downloadVideo()
        Bd.downloadAudio()
        Bd.Convert()
        Bd.clean()
    else:
        Bd.downloadVideo()
        if len(videoCache)>1:
            Bd.Convert_concat()
            Bd.clean2()




if __name__ == '__main__':
    main()