import discord
from discord.ext import commands
import youtube_dl
import asyncio

class musicyt(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.is_playing=False
        self.FFMPEG_OPTIONS={
          'before_options':
          '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        self.YDL_OPTIONS={'format': 'bestaudio','no_playlist':'True'}
        self.music_queue = []
        self.vc=""
        self.ctx=""
        self.voice=""


    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        await ctx.send('Paused ⏸︎')
        await ctx.voice_client.pause()
        

    @commands.command()
    async def resume(self, ctx):
        await ctx.send('Resume ▶️')
        await ctx.voice_client.resume()
        

    def search_yt(self,item):
      with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
        try:
          info = ydl.extract_info("ytsearch:%s"% item,download=False)['entries'][0]
          url2=info['formats'][0]['url']
          print('url2='+url2)
          title=info['title']
          duration=info['duration']
          duration1=str(duration)
        except Exception:
          return False
      return{'source':info['formats'][0]['url'],'title':info['title'],'duration':duration1}

    
    def search_ytl(self,url):
      with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
        try:
          info = ydl.extract_info(url,download=False)
          url2= info['formats'][0]['url']
          print("url2="+url2)
          title= info['title']
          print("title="+title)
          duration=info['duration']
          duration1=str(duration)
        except Exception:
          return False
      return{'source':url2,'title':title,'duration':duration1}


    async def play_next(self):
      if len(self.music_queue)>0:
        self.is_playing=True
        m_url=self.music_queue[0][0]['source']
        t=self.music_queue[0][0]['duration']
        i=0
        curr=""
        next=""
        currdur=""
        curr+=self.music_queue[i][0]['title']
        currdur+=self.music_queue[i][0]['duration']
        self.music_queue.pop(0)
        currduration=int(currdur)
        sec1=currduration%60
        sec1=int(sec1)
        min1=((currduration/60)-(sec1/60))
        min1=int(min1)
        hrs1=((currduration/3600)-(min1/60)-(sec1/3600))
        hrs1=int(hrs1)
        sec=str(sec1)
        min=str(min1)
        hrs=str(hrs1)
        print(len(self.music_queue))
        if len(self.music_queue)==0:
          next+="No more Songs"
        else:
          next+=self.music_queue[i][0]['title']
        embed=discord.Embed(title="Now Playing",color=0x00ff00)
        if hrs=='0':
          if min=='0':
            embed.add_field(name=curr, value="Duration: "+sec+" secs ",inline=False)
          else:
            embed.add_field(name=curr, value="Duration: "+min+" mins "+sec+" secs ",inline=False)
        else:
          embed.add_field(name=curr, value="Duration: "+hrs+" hrs "+min+" mins "+sec+" secs",inline=False)
        embed.add_field(name="Up Next",value=next)
        await self.ctx.send(embed=embed)
        
        self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS))
        self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS))
        t=int(t)
        t=t+3
        await asyncio.sleep(t)
        
        await self.play_next()
      else:
        self.is_playing=False


    async def play_music(self):
            if len(self.music_queue)>0:
              if self.is_playing!=True:
                self.is_playing=True
                
                if self.vc == "" or not self.vc.is_connected():
                  self.vc=await self.music_queue[0][1].connect()
                else:
                  voice_channel=self.ctx.author.voice.channel
                  
                  print(voice_channel)
                  print(self.voice)
                  if voice_channel!=self.voice:
                    self.vc=await self.client.move_to(self.music_queue[0][1])
              m_url=self.music_queue[0][0]['source']
              t=self.music_queue[0][0]['duration']
              i=0
              curr=""
              next=""
              currdur=""
              curr+=self.music_queue[i][0]['title']
              currdur+=self.music_queue[i][0]['duration']
              self.music_queue.pop(0)
              currduration=int(currdur)
              sec1=currduration%60
              sec1=int(sec1)
              min1=((currduration/60)-(sec1/60))
              min1=int(min1)
              hrs1=((currduration/3600)-(min1/60)-(sec1/3600))
              hrs1=int(hrs1)
              sec=str(sec1)
              min=str(min1)
              hrs=str(hrs1)
              print(len(self.music_queue))
              if len(self.music_queue)==0:
                next+="No more Songs"
              else:
                next+=self.music_queue[i][0]['title']
              embed=discord.Embed(title="Now Playing",color=0x00ff00)
              if hrs=='0':
                if min=='0':
                  embed.add_field(name=curr, value="Duration: "+sec+" secs ",inline=False)
                else:
                  embed.add_field(name=curr, value="Duration: "+min+" mins "+sec+" secs ",inline=False)
              else:
                embed.add_field(name=curr, value="Duration: "+hrs+" hrs "+min+" mins "+sec+" secs",inline=False)
              embed.add_field(name="Up Next",value=next)
              await self.ctx.send(embed=embed)
              self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS))
              
              t=int(t)
              t=t+3
              await asyncio.sleep(t)
              await self.play_next()
            else:
              self.is_playing=False
    
    
    @commands.command()
    async def play(self,ctx, *args):
      query=" ".join(args)
      
      if ctx.author.voice is None:
        await ctx.send("You're Not in a voice channel")
      else:
        voice_channel=ctx.author.voice.channel
        self.ctx=ctx
        self.voice=voice_channel
        if "https://" in query:
          print("It is a link")
          song=self.search_ytl(query)
        else:
          print("it is not a link")
          song=self.search_yt(query)

        if type(song)==type(True):
          await ctx.send("Could not play the song.This could be due to a playlist")
        else:
          await ctx.send("Song added to the queue")
          self.music_queue.append([song,voice_channel])
          i=0
          curr=""
          next=""
          currdur=""
          curr+=song['title']
          currdur+=song['duration']
          currduration=int(currdur)
          sec1=currduration%60
          sec1=int(sec1)
          min1=((currduration/60)-(sec1/60))
          min1=int(min1)
          hrs1=((currduration/3600)-(min1/60)-(sec1/3600))
          hrs1=int(hrs1)
          sec=str(sec1)
          min=str(min1)
          hrs=str(hrs1)
          embed=discord.Embed(title="Added to Queue",color=0x00ff00)
          if hrs=='0':
            if min=='0':
              embed.add_field(name=curr, value="Duration: "+sec+" secs ",inline=False)
            else:
              embed.add_field(name=curr, value="Duration: "+min+" mins "+sec+" secs ",inline=False)
          else:
            embed.add_field(name=curr, value="Duration: "+hrs+" hrs "+min+" mins "+sec+" secs",inline=False)
          await ctx.send(embed=embed)
          if self.is_playing==False:
            await self.play_music()

    @commands.command()
    async def queue(self, ctx):
      embed=discord.Embed(title="Queue",color=0xBB30AF)
      if len(self.music_queue)>0:
        for j in range(0,len(self.music_queue)):
          s=j+1
          curr=""
          currdur=""
          curr+=self.music_queue[j][0]['title']
          currdur+=self.music_queue[j][0]['duration']
          currduration=int(currdur)
          sec1=currduration%60
          sec1=int(sec1)
          min1=((currduration/60)-(sec1/60))
          min1=int(min1)
          hrs1=((currduration/3600)-(min1/60)-(sec1/3600))
          hrs1=int(hrs1)
          sec=str(sec1)
          min=str(min1)
          hrs=str(hrs1)
          if hrs=='0':
            if min=='0':
              embed.add_field(name=curr, value="Duration: "+sec+" secs ",inline=False)
            else:
              embed.add_field(name=curr, value="Duration: "+min+" mins "+sec+" secs ",inline=False)
          else:
            embed.add_field(name=curr, value="Duration: "+hrs+" hrs "+min+" mins "+sec+" secs",inline=False)

      else:
        embed.add_field("No music in the queue")
      await ctx.send(embed=embed)
      
    
    @commands.command()
    async def skip(self,ctx):
      if self.vc!="":
        self.vc.stop()
        await self.play_music()

    @commands.command()
    async def playlist(self,ctx,url):
      voice_channel=ctx.author.voice.channel
      self.ctx=ctx
      self.voice=voice_channel
      a=0
      with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
        try:
          info = ydl.extract_info(url,download=False)
          print(info)
          if 'entries' in info: 
            print("1")
            for i in info['entries']:
              print("2")
              url2 = info['formats'][i]['url']
              print("url2"+ url2)
          print(a)          

      

              
        except Exception:
          return False
      if self.is_playing==False:
        await self.play_music()

def setup(client):
    client.add_cog(musicyt(client))
