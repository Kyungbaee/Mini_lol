# 필요한 라이브러리
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

# ...으로 안보이는 row 모두 보이게하기
pd.options.display.max_rows = None


"""
(지역, 티어, 포지션) 입력 시 해당 포지션 챔피언들의 상대 픽 추천(Top3) - 이름순
입력 예시 : league_of_legend("kr","platinum_plus","Top")
"""
def league_of_legend(region,tier,position):
    base_url = f"https://www.op.gg/champions?region={region}&tier={tier}&position={position}"
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'}
    response = requests.get(base_url,headers=headers)
    html = bs(response.text,"lxml")
    a_list = html.select("#content-container > div.css-1fcwcq0.e2v0byd0 > main > div> table >tbody > tr >td")

    champ_list = [str(a_list[(7*index+1)]).split("strong>")[1][:-2] for index in range(int(len(a_list)/7))]

    counter_total = []
    win_rate = []
    pick_rate = []
    ban_rate = []

    index = 1
    while(len(a_list)>(7*index-1)):
        counter_list = [str(a_list[(7*index-1)].select("img")).split("img alt=\"")[1:][i].split("\" class")[0] for i in range(3)]
        win_rate.append(float(str(a_list[(7*index-4)]).split(">")[1].split("<")[0]))
        pick_rate.append(float(str(a_list[(7*index-3)]).split(">")[1].split("<")[0]))
        ban_rate.append(float(str(a_list[(7*index-2)]).split(">")[1].split("<")[0]))
        counter_total.append(str(counter_list))

        index +=1

    df_champ = pd.DataFrame(champ_list,columns=[f"{position}"])
#     df_champ["Win Rate"] = win_rate
#     df_champ["Pick Rate"] = pick_rate
#     df_champ["Ban Rate"] = ban_rate
    df_champ["Recommend"] = counter_total

    return df_champ

  
"""
포지션, 챔피언명 입력 시 해당 포지션 챔피언의 상대 픽 추천(Top3)
입력 예시 : recommend("Mid","Akali")
"""  
def recommend(position, champion):
    df_top = league_of_legend("kr","platinum_plus",f"{position}")
    rec = df_top[df_top[f"{position}"] == f"{champion}"]["Recommend"].iloc[0]
    return rec

  
  
"""
전 포지션 챔피언들의 상대 픽 추천(Top3) - 이름순
입력 예시 : all_list()
"""  
def all_list():
    position_list = ["Top","Jungle","Mid","Adc","Support"]
    df = pd.DataFrame()
    for position in position_list:
        if df.empty:
            df = league_of_legend("kr","platinum",position)
        else :
            df = pd.concat([df,league_of_legend("kr","platinum",position)],axis=1)
    return df

  
"""
입력한 포지션, 챔피언의 상대전적 - 승률순
입력 예시 : match_up("Jungle","Poppy")
"""    
def match_up(position,champion):
    match_up = pd.DataFrame(columns=["My champ"])
    base_url2 = f"https://www.op.gg/champions/{champion}/{position}/counters?region=kr&tier=platinum_plus"
    response2 = requests.get(base_url2,headers=headers)
    html2 = bs(response2.text,"lxml")
    b_list = html2.select("#content-container > aside > div.css-1o4rcgx.e5r18j22 > div > div > table > tbody > tr > td > div > div")
    c_list = html2.select("#content-container > aside > div.css-1o4rcgx.e5r18j22 > div > div > table > tbody > tr > td.css-1wvfkid.exo2f211 > span")
    
    percent_list = [str(percent).split(">")[1].split("<")[0] for percent in c_list]
    percent_series = pd.Series(percent_list,name="Win rate")
    name_list= [str(name).split(">")[2][:-5] for name in b_list[1::2]]
    name_series = pd.Series(name_list,name="Target")
    
    match_up["My champ"] = [f"{champion}"]
    match_up = pd.concat([match_up,percent_series],axis=1)
    match_up = pd.concat([match_up,name_series],axis=1)
    match_up = match_up.fillna(method='ffill').sort_values("Win rate",ascending=False)
    return match_up
