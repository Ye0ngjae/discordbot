import asyncio
import discord #디스코드
import urllib #크롤링
from bs4 import BeautifulSoup #클로링
import nipy #급식, 학사일정 파서(외부 라이브러리)
from time import localtime, strftime #일시 지정

#만든이 : 인천 백석중학교 30220 남영재


cal = nipy.Scalendar("인천","E100000770", "3")

#급식파서 세팅


photo = 'http://baksuk.icems.kr/images/template/00779/common/logo.gif'
home = 'http://baksuk.icems.kr'

#임베드 url 초기 세팅

client = discord.Client()

#디스코드 초기 세팅



@client.event
async def on_ready():

    game = discord.Game("도움말 명령어는 //help")
    await client.change_presence(status=discord.Status.online, activity=game)
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print("=" * 20)

    #세팅 기록


@client.event
async def on_message(message):
    if message.author.bot:
        return None

    if message.content.startswith('//help'):
        channel = message.channel
        embed1 = discord.Embed(title='명령어', description='봇 명령어입니다')
        embed1.add_field(name='//공지사항', value='현재 최신 공지사항을 불러옵니다', inline=False)
        embed1.add_field(name='//학교소식', value='현재 최신 학교소식을 불러옵니다', inline=False)
        embed1.add_field(name='//급식', value='오늘 급식을 불러옵니다', inline=False)
        embed1.add_field(name='//학사일정', value='한 달 동안의 학사일정을 불러옵니다', inline=False)
        embed1.set_thumbnail(url=photo)
        embed1.set_footer(text='버그제보:남영재#4967')
        await channel.send(embed=embed1)
    
    #명령어 설명
    
    if message.content.startswith('//공지사항'):
        url = 'http://baksuk.icems.kr/boardCnts/list.do?boardID=9702&m=0201'
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html5lib')
        table = soup.find('table', {'class': 'bbsList'}) 

        for tbodys in table.find_all('tbody'): 
            trslist = list(tbodys.find_all('tr')) 
            tdslist = trslist[1]
            tds = list(tdslist.find_all('td')) 

        for td in tds: 
            if td.find('a'):
                num1 = tds[0].text 
                subject = td.find('a').text 
                write = tds[2].text 
                date = tds[4].text 

        channel = message.channel
        embed1 = discord.Embed(title='공지사항',description='현재 최신 공지사항입니다',url=url)
        embed1.add_field(name='번호',value=num1+'번',inline=False)
        embed1.add_field(name='제목', value=subject,inline=False)
        embed1.add_field(name="글쓴이",value=write,inline=False)
        embed1.set_footer(text='작성일 '+date)
        embed1.set_thumbnail(url=photo)
        await channel.send(embed=embed1)

    #공지사항 출력

    if message.content.startswith('//학교소식'):
        url = 'http://baksuk.icems.kr/boardCnts/list.do?boardID=254241&m=10&s=baksuk'
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html5lib')
        table = soup.find('table', {'class': 'bbsList'})

        for tbodys in table.find_all('tbody'):
            trslist = list(tbodys.find_all('tr'))
            tdslist = trslist[0]
            tds = list(tdslist.find_all('td'))

        for td in tds:
            if td.find('a'):
                num1 = tds[0].text
                subject = td.find('a').text 
                write = tds[2].text 
                date = tds[4].text 

        channel = message.channel
        embed1 = discord.Embed(title='학교소식',description='현재 최신 학교소식입니다',url=url)
        embed1.add_field(name='번호',value=num1+'번',inline=False)
        embed1.add_field(name='제목', value=subject,inline=False)
        embed1.add_field(name="글쓴이",value=write,inline=False)
        embed1.set_footer(text='작성일 '+date)
        embed1.set_thumbnail(url=photo)
        await channel.send(embed=embed1)
    
    #학교 소식 출력

    if message.content.startswith('//급식'):
        meal = nipy.Smeal("인천", "E100000770", "3") #급식 정보 불러오기 
        channel = message.channel
        y = strftime("%Y")
        m = strftime("%m")
        d = strftime("%d")
        meal = meal.day(y, m, d, "2")
        meal = meal.split("<br/>", -1)
        embed1 = discord.Embed(title='{}년 {}월 {}일 급식'.format(y,m,d))
        count = len(meal)

        for i in range(count - 1):
            embed1.add_field(name=meal[i],value='.', inline=False)
        
        embed1.set_footer(text='')
        embed1.set_thumbnail(url=photo)
        await channel.send(embed=embed1)

    #급식 출력

    if message.content.startswith('//학사일정'):
        channel = message.channel
        y = strftime("%Y")
        m = strftime("%m")
        d = strftime("%d")
        plan = cal.month(y,m)
        embed1 = discord.Embed(title="{}년 {}월 학사일정".format(y,m))

        for key in plan.keys():
            embed1.add_field(name = "{} : {}".format(key,plan[key]), value='.', inline=False)
        
        embed1.set_footer(text='')
        embed1.set_thumbnail(url=photo)
        await channel.send(embed=embed1)

    #학사일정 출력



tk = 'ODUyMTM1MDIyNTU4NzA3NzMz.{}'.format('YMCalQ.oMJHOUHqTAtrssMKGJ6BFTREUog')
client.run(tk)
