import random

import discord
from discord.ext import commands, tasks
from ERBSClient import ErbsClient
from discord_bot_data import *

TOKEN = 'ODA5MDQ4OTY3ODQwMDA2MTQ1.GdOWuP.TYhB22RimQHtFtRhOFD6JxJXNbgMQZTNWFkLYA'
BOT_PREFIX=('/')
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=discord.Intents.all())

api_key_file = open('api_key')  # file containing one line of the ER:BS api key
private_api_key = api_key_file.readline().rstrip()
api_client = ErbsClient(api_key=private_api_key, version='v1')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async  def rank(ctx,*,message:str):
    #embedVar = search_user_ranking(message.split()[1])
    embedVar = search_user_ranking(message.split()[0])
    await ctx.send(embed=embedVar)

@bot.command()
async def 랭크(ctx,*,message:str):
    message=f'{message}'
    await rank(ctx,message=message)

@bot.command()
async def normal(ctx,*,message:str):
    embedVar=search_user_normal(message.split()[0])
    await ctx.send(embed=embedVar)

@bot.command()
async def 노말(ctx,*,message:str):
    message= f'{message}'
    await normal(ctx,message=message)

@bot.command()
async def gamehis(ctx,*,message:str):
    embedVar=search_user_games(message.split()[0])
    await ctx.send(embed=embedVar)

@bot.command()
async def 전적(ctx,*,message:str):
    message = f'{message}'
    await gamehis(ctx, message=message)

@bot.command()
async def most(ctx,*,message:str):
    embedVar=search_user_most(message.split()[0])
    await ctx.send(embed=embedVar)

@bot.command()
async def 모스트(ctx,*,message:str):
    message = f'{message}'
    await most(ctx, message=message)

@bot.command()
async def 이리도움말(ctx):
    embedVar = discord.Embed(title='명령어 목록', color=0x0db6e0)
    embedVar.add_field(name='/rank [닉네임], /랭크 [닉네임]', value='랭크 게임 정보를 보여줍니다', inline=False)
    embedVar.add_field(name='/normal [닉네임], /노말 [닉네임]', value='노말 게임 정보를 보여줍니다', inline=False)
    embedVar.add_field(name='/gamehis [닉네임], /전적 [닉네임]', value='최근 10게임 전적을 보여줍니다', inline=False)
    embedVar.add_field(name='/most [닉네임], /모스트 [닉네임]', value='랭크에서의 캐릭터 모스트 top3정보를 보여줍니다', inline=False)

    await ctx.send(embed=embedVar)

def search_user_most(nickname):
    if not nickname:
        return
    user_num = api_client.get_user_num(nickname)

    character_code=[0,0,0]
    usages=[0,0,0]
    max_kill=[0,0,0]
    top1=[0,0,0]
    top3=[0,0,0]
    average_rank=[0,0,0]

    ranked_user_stats = api_client.get_user_stats(user_num, SEASON_10)

    for i in range(3):
        try:
            character_code[i] = int(ranked_user_stats['userStats'][0]['characterStats'][i]['characterCode'])
            usages[i]=int(ranked_user_stats['userStats'][0]['characterStats'][i]['usages'])
            max_kill[i]=int(ranked_user_stats['userStats'][0]['characterStats'][i]['maxKillings'])
            top3[i]=int(ranked_user_stats['userStats'][0]['characterStats'][i]['top3'])
            top1[i]=int(ranked_user_stats['userStats'][0]['characterStats'][i]['wins'])
            average_rank[i]=int(ranked_user_stats['userStats'][0]['characterStats'][i]['averageRank'])
            print(character_code[i])
            print(i)
        except:
            embedVar = discord.Embed(title=nickname.upper(), description='랭크 정보가 없습니다', color=0x0db6e0)
            return embedVar
            pass

    embedVar = discord.Embed(title=nickname.upper(), color=0x0db6e0)
    embedVar.set_thumbnail(url=COMMON_STRINGS_DICT[str(character_code[0])])

    for i in range(3):
        embedVar.add_field(name='캐릭터', value='{0}'.format(CHARACTER_LIST[int(character_code[i])]), inline=True)
        embedVar.add_field(name='플레이 수', value='{0}회'.format(usages[i]), inline=True)
        embedVar.add_field(name='최다 킬', value='{0}킬'.format(max_kill[i]), inline=True)
        if(usages[i]==0):
            embedVar.add_field(name='top3 확률', value='{0}%'.format(0), inline=True)
        else:
            embedVar.add_field(name='top3 확률', value='{0}%'.format(round(float(top3[i]/usages[i]*100),2)), inline=True)
        embedVar.add_field(name='top1 횟수', value='{0}회'.format(top1[i]), inline=True)
        embedVar.add_field(name='평균등수', value='{0}등'.format(average_rank[i]), inline=True)
        embedVar.add_field(name='',value='',inline=False)
    return embedVar

def search_user_ranking(nickname):
    if not nickname:
        return
    user_num = api_client.get_user_num(nickname)

    # ranked_mmr = [0, 0, 0]
    # normal_mmr = [0, 0, 0]
    ranked_mmr=0
    normal_mmr=0
    most_character_code=0
    ranking_percent=0
    average_kill=0
    average_hunt=0
    top1_percent=0.0

    # fetch and parse ranked game stats
    ranked_user_stats = api_client.get_user_stats(user_num, SEASON_10)

    # for i in range(3):
    #     try:
    #         matching_team_mode = int(ranked_user_stats['userStats'][i]['matchingTeamMode'])
    #         ranked_mmr[matching_team_mode - 1] = ranked_user_stats['userStats'][i]['mmr']
    #     except:
    #         pass
    try:
        #print(ranked_user_stats['userStats'][0]['mmr'])
        ranked_mmr = ranked_user_stats['userStats'][0]['mmr']
        most_character_code = ranked_user_stats['userStats'][0]['characterStats'][0]['characterCode']
        ranking_percent = ranked_user_stats['userStats'][0]['rankPercent']
        average_kill = ranked_user_stats['userStats'][0]['averageKills']
        average_hunt = ranked_user_stats['userStats'][0]['averageHunts']
        top1_percent = ranked_user_stats['userStats'][0]['top1']

        #print(most_character_code)
        if most_character_code>68:
            most_character_code=100
    except:
        embedVar = discord.Embed(title=nickname.upper(),description='랭크 정보가 없습니다', color=0x0db6e0)
        return embedVar
        pass

    embedVar = discord.Embed(title=nickname.upper(), color=0x0db6e0)
    embedVar.set_thumbnail(url=COMMON_STRINGS_DICT[str(most_character_code)])
    embedVar.add_field(name='Season 1.0 랭크', value=get_tier(ranked_mmr), inline=True)
    embedVar.add_field(name='상위 랭킹', value='상위 {0}%'.format(ranking_percent*100), inline=False)
    embedVar.add_field(name='평균 킬수', value='{0}킬'.format(average_kill), inline=False)
    embedVar.add_field(name='평균 사냥수', value='{0}킬'.format(average_hunt), inline=False)
    embedVar.add_field(name='1등 확률', value='{0}%'.format(top1_percent*100), inline=False)
    return embedVar

def search_user_normal(nickname):
    if not nickname:
        return
    user_num = api_client.get_user_num(nickname)

    normal_user_stats = api_client.get_user_stats(user_num, NORMAL_SEASON)

    total_game = 0
    most_character_code = 0
    #ranking_percent = 0
    ranking=0
    rank_size=1
    average_rank = 0
    average_kill = 0
    average_hunt = 0
    top1_percent = 0.0


    try:
        for i in range(3):
            if(normal_user_stats['userStats'][i]['matchingTeamMode']!=3):
                continue
            else:
                total_game = normal_user_stats['userStats'][i]['totalGames']
                most_character_code = normal_user_stats['userStats'][i]['characterStats'][0]['characterCode']
                #ranking_percent = normal_user_stats['userStats'][i]['rankPercent']
                ranking=normal_user_stats['userStats'][i]['rank']
                rank_size=normal_user_stats['userStats'][i]['rankSize']
                average_rank = normal_user_stats['userStats'][i]['averageRank']
                average_kill = normal_user_stats['userStats'][i]['averageKills']
                average_hunt = normal_user_stats['userStats'][i]['averageHunts']
                top1_percent = normal_user_stats['userStats'][i]['top1']

    except:
        pass

    embedVar = discord.Embed(title=nickname.upper(), color=0x0db6e0)
    embedVar.set_thumbnail(url=COMMON_STRINGS_DICT[str(most_character_code)])
    embedVar.add_field(name='노말 게임 플레이 수', value='{0}'.format(total_game), inline=True)
    embedVar.add_field(name='상위 랭킹', value='상위 {0}%'.format(float(ranking/rank_size * 100),2), inline=False)
    embedVar.add_field(name='평균 순위', value='{0}등'.format(average_rank), inline=False)
    embedVar.add_field(name='평균 킬수', value='{0}킬'.format(average_kill), inline=False)
    embedVar.add_field(name='평균 사냥수', value='{0}킬'.format(average_hunt), inline=False)
    embedVar.add_field(name='1등 확률', value='{0}%'.format(top1_percent * 100), inline=False)
    return embedVar

def search_user_games(nickname):
    if not nickname:
        return
    user_num = api_client.get_user_num(nickname)

    # fetch and parse user games
    user_games_unparsed = api_client.get_user_games(user_num)
    user_games = user_games_unparsed['userGames']

    embedVar = discord.Embed(title='{0}의 최근 10게임 전적'.format(nickname.upper()),
                             description='(킬수,어시수,야생동물사냥수,무기숙련도)', color=0x0db6e0)
    #embedVar.set_thumbnail(url=COMMON_STRINGS_DICT['bot avatar'])

    for game in user_games:
        # check game season
        game_type = int(game['seasonId'])
        if game_type == NORMAL_SEASON:
            game_type = 'Normal'
        elif game_type == SEASON_10:
            game_type = 'Ranked'
            mmr_change = int(game['mmrGain'])
        else:
            game_type = 'unknown'

        # check game rank
        game_rank = int(game['gameRank'])

        # check game kills, assists, monster kills
        game_kills = int(game['playerKill'])
        game_assists = int(game['playerAssistant'])
        game_monster_kills = int(game['monsterKill'])
        game_weapon_level = int(game['bestWeaponLevel'])

        # check game character
        game_character = CHARACTER_LIST[int(game['characterNum'])]

        if game_type=='Ranked':
            embedVar.add_field(
                name='{0}    {1}'.format(game_type,mmr_change),
                value='{0}: 등수 #{1} - ({2}/{3}/{4}/{5})'.format(game_character, game_rank, game_kills, game_assists,
                                                                game_monster_kills, game_weapon_level),
                inline=False
            )
        else:
             embedVar.add_field(
                name='{0}'.format(game_type),
                value='{0}: 등수 #{1} - ({2}/{3}/{4}/{5})'.format(game_character, game_rank, game_kills, game_assists,
                                                              game_monster_kills,game_weapon_level),
                inline=False
            )
    return embedVar


def get_tier(mmr):
    tier = ''
    if mmr == 0:
        tier += 'Unranked'
    elif IRON_4 < mmr < IRON_3:
        tier += 'Iron 4 - {0} LP'.format(mmr % IRON_4)
    elif IRON_3 <= mmr < IRON_2:
        tier += 'Iron 3 - {0} LP'.format(mmr % IRON_3)
    elif IRON_2 <= mmr < IRON_1:
        tier += 'Iron 2 - {0} LP'.format(mmr % IRON_2)
    elif IRON_1 <= mmr < BRONZE_4:
        tier += 'Iron 1 - {0} LP'.format(mmr % IRON_1)
    elif BRONZE_4 <= mmr < BRONZE_3:
        tier += 'Bronze 4 - {0} LP'.format(mmr % BRONZE_4)
    elif BRONZE_3 <= mmr < BRONZE_2:
        tier += 'Bronze 3 - {0} LP'.format(mmr % BRONZE_3)
    elif BRONZE_2 <= mmr < BRONZE_1:
        tier += 'Bronze 2 - {0} LP'.format(mmr % BRONZE_2)
    elif BRONZE_1 <= mmr < SILVER_4:
        tier += 'Bronze 1 - {0} LP'.format(mmr % BRONZE_1)
    elif SILVER_4 <= mmr < SILVER_3:
        tier += 'Silver 4 - {0} LP'.format(mmr % SILVER_4)
    elif SILVER_3 <= mmr < SILVER_2:
        tier += 'Silver 3 - {0} LP'.format(mmr % SILVER_3)
    elif SILVER_2 <= mmr < SILVER_1:
        tier += 'Silver 2 - {0} LP'.format(mmr % SILVER_2)
    elif SILVER_1 <= mmr < GOLD_4:
        tier += 'Silver 1 - {0} LP'.format(mmr % SILVER_1)
    elif GOLD_4 <= mmr < GOLD_3:
        tier += 'Gold 4 - {0} LP'.format(mmr % GOLD_4)
    elif GOLD_3 <= mmr < GOLD_2:
        tier += 'Gold 3 - {0} LP'.format(mmr % GOLD_3)
    elif GOLD_2 <= mmr < GOLD_1:
        tier += 'Gold 2 - {0} LP'.format(mmr % GOLD_2)
    elif GOLD_1 <= mmr < PLATINUM_4:
        tier += 'Gold 1 - {0} LP'.format(mmr % GOLD_1)
    elif PLATINUM_4 <= mmr < PLATINUM_3:
        tier += 'Platinum 4 - {0} LP'.format(mmr % PLATINUM_4)
    elif PLATINUM_3 <= mmr < PLATINUM_2:
        tier += 'Platinum 3 - {0} LP'.format(mmr % PLATINUM_3)
    elif PLATINUM_2 <= mmr < PLATINUM_1:
        tier += 'Platinum 2 - {0} LP'.format(mmr % PLATINUM_2)
    elif PLATINUM_1 <= mmr < DIAMOND_4:
        tier += 'Platinum 1 - {0} LP'.format(mmr % PLATINUM_1)
    elif DIAMOND_4 <= mmr < DIAMOND_3:
        tier += 'Diamond 4 - {0} LP'.format(mmr % DIAMOND_4)
    elif DIAMOND_3 <= mmr < DIAMOND_2:
        tier += 'Diamond 3 - {0} LP'.format(mmr % DIAMOND_3)
    elif DIAMOND_2 <= mmr < DIAMOND_1:
        tier += 'Diamond 2 - {0} LP'.format(mmr % DIAMOND_2)
    elif DIAMOND_1 <= mmr < MITHRIL:
        tier += 'Diamond 1 - {0} LP'.format(mmr % DIAMOND_1)
    elif MITHRIL <= mmr < DEMIGOD:
        tier += 'Mithril - {0} LP'.format(mmr % MITHRIL)
    elif DEMIGOD <= mmr < Eternity:
        tier += 'Titan - {0} LP'.format(mmr % DEMIGOD)
    elif Eternity <= mmr:
        tier += 'Immortal - {0} LP'.format(mmr % Eternity)
    return tier

#여기 까지 이터널리턴 봇


games = {}  # {channel_id: (player1, player1_choice, player2)}

@bot.command()
async def 가위바위보(ctx, opponent: discord.Member):
    if ctx.channel.id in games:
        await ctx.send("이 채널에서 이미 게임이 진행 중입니다.")
        return
    games[ctx.channel.id] = (ctx.author, None, opponent, None)

    dm_channel_player1 = await ctx.author.create_dm()
    await dm_channel_player1.send(f"/선택 가위, /선택 바위, /선택 보 중 하나를 DM으로 보내주세요!")

    dm_channel = await opponent.create_dm()
    await dm_channel.send(f"{ctx.author.mention}님이 가위바위보 게임을 신청하셨습니다. /선택 가위, /선택 바위, /선택 보 중 하나를 DM으로 보내주세요!")
    await ctx.send(f"{opponent.mention}, /선택 가위, /선택 바위, /선택 보 중 하나를 DM으로 보내주세요!")

@bot.command()
async def 선택(ctx, choice):
    # DM에서만 작동
    if not isinstance(ctx.channel, discord.DMChannel):
        print('1')
        return

    # 사용자의 선택을 games 딕셔너리에서 찾기
    game_channel_id = None
    for channel_id, (player1, player1_choice, player2, player2_choice) in games.items():
        if ctx.author == player1 or ctx.author == player2:
            print(2)
            game_channel_id = channel_id
            break

    # 해당 게임이 존재하지 않으면 종료
    if game_channel_id is None:
        await ctx.send("게임이 존재하지 않습니다.")
        return

    player1, player1_choice, player2, player2_choice = games[game_channel_id]

    if ctx.author == player1:
        player1_choice = choice
    elif ctx.author == player2:
        player2_choice = choice

        # 두 플레이어 모두 선택을 했다면 결과를 계산
    if player1_choice and player2_choice:
        result = determine_winner(player1_choice, player2_choice, player1.display_name, player2.display_name)
        game_channel = bot.get_channel(game_channel_id)
        await game_channel.send(result)
        del games[game_channel_id]
    else:
        games[game_channel_id] = (player1, player1_choice, player2, player2_choice)


# @bot.command()
# async def 선택(ctx, choice):
#     choice=f'{choice}'
#     await choose(ctx,choice=choice)


def determine_winner(choice1, choice2, player1_name, player2_name):
    if choice1 == choice2:
        return "무승부!"
    if (choice1 == "가위" and choice2 == "보") or (choice1 == "바위" and choice2 == "가위") or (choice1 == "보" and choice2 == "바위"):
        return f"{choice1} 선택! 승자는 {player1_name}입니다!"
    return f"{choice2} 선택! 승자는 {player2_name}입니다!"

#역할 랜덤 코드
roles = ['탑', '정글', '미드', '원딜', '서폿']

@bot.command()
async def assign(ctx, name1: str, name2: str, name3: str, name4: str, name5: str):
    names = [name1, name2, name3, name4, name5]
    random.shuffle(names)

    embedVar = discord.Embed(title='랜덤 포지션', color=0x0db6e0)
    for i in range(5):
        embedVar.add_field(name='{0}'.format(roles[i]),value='{0}'.format(names[i]),inline=False)

    await ctx.send(embed=embedVar)

@bot.command()
async def 랜덤포지션(ctx, name1: str, name2: str, name3: str, name4: str, name5: str):
    await assign(ctx,name1,name2,name3,name4,name5)

@bot.command()
async def 내전도움말(ctx):
    embedVar = discord.Embed(title='명령어 목록', color=0x0db6e0)
    embedVar.add_field(name='/가위바위보 @[닉네임]', value='가위바위보게임을 시작합니다', inline=False)
    embedVar.add_field(name='/선택 [가위,바위,보]', value='봇에게 개인메세지로 가위바위보를 전달합니다(개인메세지로 주셔야합니다)', inline=False)
    embedVar.add_field(name='/랜덤포지션 [닉네임] [닉네임] [닉네임] [닉네임] [닉네임]', value='5명의 포지션을 랜덤으로 정해줍니다', inline=False)

    await ctx.send(embed=embedVar)



#메이플 정보 코드

maple_color =0xFF8C00

@bot.command()
async def 메이플도움말(ctx):
    embedVar = discord.Embed(title='명령어 목록', color=maple_color)
    embedVar.add_field(name='/종료이벤트', value='메이플 이벤트 종료일정을 보여줍니다', inline=False)
    embedVar.add_field(name='/예정이벤트', value='메이플 예정 이벤트를 보여줍니다', inline=False)
    await ctx.send(embed=embedVar)
@bot.command()
async def 종료이벤트(ctx):
    embedVar = maple_info_eventend()
    await ctx.send(embed=embedVar)

def maple_info_eventend():
    embedVar = discord.Embed(title='종료 예정 이벤트', color=maple_color)
    embedVar.set_thumbnail(url=COMMON_STRINGS_DICT['maple_thumbnail1'])
    embedVar.add_field(name='버닝 월드 리프', value='9월 13일(수)까지만 가능. 이후 삭제', inline=False)
    embedVar.add_field(name='캐시 패키지 일부 판매종료',
                       value='핑크/그레이 네로패키지, 블레어 쿼츠/펄리 헤어, 로얄스타일, 로얄 헤어 9월 13일 까지만 판매', inline=False)
    embedVar.add_field(name='pc방 접속이벤트', value='9월 21일(목)까지 수령가능', inline=False)
    return embedVar

@bot.command()
async def 예정이벤트(ctx):
    embedVar = maple_info_event()
    await ctx.send(embed=embedVar)

def maple_info_event():
    embedVar = discord.Embed(title='예정 이벤트', color=maple_color)
    embedVar.set_thumbnail(url=COMMON_STRINGS_DICT['maple_thumbnail2'])
    embedVar.add_field(name='전문기술개선',
                       value='모든 전문기술 배우는거 가능 \n장인 이상 등급에서 숙련도 하락x\n채집맵이 개인화', inline=False)
    embedVar.add_field(name='코디 염색 시스템 출시예정',
                       value='코디템을 염색할수 있는 쿠폰 출시예정(추석 패키지티켓으로 획득 가능성 농후)', inline=False)
    embedVar.add_field(name='추석이벤트',
                       value='큐브팩 출시, 추석패키지 티켓 출시예상. 14일 테섭, 21일 본섭적용', inline=False)
    embedVar.add_field(name='캐시이동', value='9월 22일(금)10시~9월 29일(금)10시', inline=False)
    return embedVar



bot.run(TOKEN)


'''
테스트용 샘플
래빗다이스
422281

'''