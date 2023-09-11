import random

import discord
from discord.ext import commands, tasks
from ERBSClient import ErbsClient
from discord_bot_data import *

TOKEN = ''
BOT_PREFIX=('!')
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
async def games(ctx,*,message:str):
    embedVar=search_user_games(message.split()[0])
    await ctx.send(embed=embedVar)

@bot.command()
async def 전적(ctx,*,message:str):
    await games(ctx,message)

# @bot.command()
# async def most(ctx,*,message:str):
#     embedVar=search_user_ranking(message.split()[0])
#     await ctx.send(embed=embedVar)

@bot.command()
async def erhelp(ctx):
    embedVar = discord.Embed(title='명령어 목록', color=0x0db6e0)
    embedVar.add_field(name='!rank [닉네임], !랭크 [닉네임]', value='랭크 게임 정보를 보여줍니다', inline=False)
    embedVar.add_field(name='!normal [닉네임], !노말 [닉네임]', value='노말 게임 정보를 보여줍니다', inline=False)
    embedVar.add_field(name='!games [닉네임], !전적 [닉네임]', value='최근 10게임 전적을 보여줍니다', inline=False)

    await ctx.send(embed=embedVar)

def search_user_most(nickname):
    if not nickname:
        return
    user_num = api_client.get_user_num(nickname)




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
    ranking_percent = 0
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
                ranking_percent = normal_user_stats['userStats'][i]['rankPercent']
                average_rank = normal_user_stats['userStats'][i]['averageRank']
                average_kill = normal_user_stats['userStats'][i]['averageKills']
                average_hunt = normal_user_stats['userStats'][i]['averageHunts']
                top1_percent = normal_user_stats['userStats'][i]['top1']

    except:
        pass

    embedVar = discord.Embed(title=nickname.upper(), color=0x0db6e0)
    embedVar.set_thumbnail(url=COMMON_STRINGS_DICT[str(most_character_code)])
    embedVar.add_field(name='노말 게임 플레이 수', value='{0}'.format(total_game), inline=True)
    embedVar.add_field(name='상위 랭킹', value='상위 {0}%'.format(ranking_percent * 100), inline=False)
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
        else:
            game_type = 'unknown'
        # elif game_type == SEASON_1:
        #     game_type = 'Ranked (Season 1)'
        # elif game_type == PRE_SEASON_2:
        #     game_type = 'Ranked (Pre-Season 2)'
        # elif game_type == SEASON_2:
        #     game_type = 'Ranked (Season 2)'
        # elif game_type == PRE_SEASON_3:
        #     game_type = 'Ranked (Pre-Season 3)'
        # elif game_type == SEASON_3:
        #     game_type = 'Ranked'
        # elif game_type == PRE_SEASON_4:
        #     game_type = 'Ranked (Pre-Season 4)'
        # elif game_type == SEASON_4:
        #     game_type = 'Ranked'

        # # check game mode
        # game_team_mode = int(game['matchingTeamMode'])
        # if game_team_mode == SOLO_MODE:
        #     game_team_mode = 'Solo'
        # elif game_team_mode == DUO_MODE:
        #     game_team_mode = 'Duo'
        # elif game_team_mode == SQUAD_MODE:
        #     game_team_mode = 'Squad'

        # check game rank
        game_rank = int(game['gameRank'])

        # check game kills, assists, monster kills
        game_kills = int(game['playerKill'])
        game_assists = int(game['playerAssistant'])
        game_monster_kills = int(game['monsterKill'])
        game_weapon_level = int(game['bestWeaponLevel'])

        # check game character
        game_character = CHARACTER_LIST[int(game['characterNum'])]

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
        tier += 'Diamond 1 - {0} LP'.format(mmr % DIAMOND_1)
    elif DEMIGOD <= mmr < Eternity:
        tier += 'Titan - {0} LP'.format(mmr % DEMIGOD)
    elif Eternity <= mmr:
        tier += 'Immortal - {0} LP'.format(mmr % Eternity)
    return tier

#여기 까지 이터널리턴 봇


games = {}  # {channel_id: (player1, player1_choice, player2)}

@bot.command()
async def start(ctx, opponent: discord.Member):
    if ctx.channel.id in games:
        await ctx.send("이 채널에서 이미 게임이 진행 중입니다.")
        return
    games[ctx.channel.id] = (ctx.author, None, opponent)
    await ctx.send(f"{opponent.mention}, 가위, 바위, 보 중 하나를 선택하세요!")

@bot.command()
async def 가위바위보(ctx, opponent: discord.Member):
    await start(ctx, opponent)


@bot.command()
async def choose(ctx, choice):
    if ctx.channel.id not in games:
        return

    player1, player1_choice, player2 = games[ctx.channel.id]

    if ctx.author == player1:
        games[ctx.channel.id] = (player1, choice, player2)
    elif ctx.author == player2:
        if not player1_choice:
            await ctx.send("다른 플레이어가 아직 선택하지 않았습니다.")
            return
        result = determine_winner(player1_choice, choice, player1.display_name, player2.display_name)
        await ctx.send(result)
        del games[ctx.channel.id]

@bot.command()
async def 선택(ctx, choice):
    await choose(ctx,choice)

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
        print('{0}'.format(roles[i]))
        print('{0}'.format(names[i]))
        embedVar.add_field(name='{0}'.format(roles[i]),value='{0}'.format(names[i]),inline=False)


    #message = "\n".join([f"{role}: {name}" for role, name in assignment.items()])
    await ctx.send(embed=embedVar)

bot.run(TOKEN)


'''
테스트용 샘플
래빗다이스
422281

'''