import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import seaborn as sns
import matplotlib.pyplot as plt
from urllib import parse

pd.options.display.max_rows = None

# 데이터 시각화 도구에서 한글을 그대로 출력하게 되면 글자가 깨져서 나오게 되기 때문에 글꼴설정을 합니다.
def get_font_family():
    """
    시스템 환경에 따른 기본 폰트명을 반환하는 함수
    """
    import platform
    system_name = platform.system()
    # colab 사용자는 system_name이 'Linux'로 확인

    if system_name == "Darwin" :
        font_family = "AppleGothic"
    elif system_name == "Windows":
        font_family = "Malgun Gothic"
    else:
        # Linux
        !apt-get install fonts-nanum -qq  > /dev/null
        !fc-cache -fv

        import matplotlib as mpl
        mpl.font_manager._rebuild()
        findfont = mpl.font_manager.fontManager.findfont
        mpl.font_manager.findfont = findfont
        mpl.backends.backend_agg.findfont = findfont
        
        font_family = "NanumBarunGothic"
    return font_family

# 위에서 만든 함수를 통해 시스템 폰트를 불러옵니다.
get_font_family()

# 시각화를 위한 폰트설정
# 위에서 만든 함수를 통해 시스템 폰트를 불러와서 font_family라는 변수에 할당합니다.

plt.style.use("ggplot")

font_family = get_font_family()
# 폰트설정

plt.rc("font", family=font_family)
# 마이너스 폰트 설정

plt.rc("axes", unicode_minus=False)
# 그래프에 retina display 적용

from IPython.display import set_matplotlib_formats
set_matplotlib_formats("retina")

# ...으로 안보이는 row 모두 보이게하기
pd.options.display.max_rows = None

# 챔피언 이름 전처리
champ_name = {"Kai'Sa": "Kaisa"
              , "Wukong":"monkeyking"
              , "Lee Sin":"LeeSin"
              ,"Kha'Zix" :"khazix"
              ,"Renata Glasc" : "renata"
             }

"""
소환사 명 입력 받기
"""
name = input("소환사명 입력 : ")
summoners_name = parse.quote(f'{name}')

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
    try:
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'}
        match_up = pd.DataFrame(columns=["champ"])
        
        if champion in champ_name :
            champion = champ_name.get(champion)
            
        champion = champion.lower().replace(" ","")
        base_url2 = f"https://www.op.gg/champions/{champion}/{position}/counters?region=kr&tier=all"
        response2 = requests.get(base_url2,headers=headers)
        html2 = bs(response2.text,"lxml")
        b_list = html2.select("#content-container > aside > div.css-1o4rcgx.e5r18j22 > div > div > table > tbody > tr > td > div > div")
        c_list = html2.select("#content-container > aside > div.css-1o4rcgx.e5r18j22 > div > div > table > tbody > tr > td.css-1wvfkid.exo2f211 > span")
        
        
        percent_list = [str(percent).split(">")[1].split("<")[0] for percent in c_list]
        percent_series = pd.Series(percent_list,name="Win rate")
        name_list= [str(name).split(">")[2][:-5] for name in b_list[1::2]]
        name_series = pd.Series(name_list,name="Target")

        match_up["champ"] = [f"{champion}"]
        match_up = pd.concat([match_up,percent_series],axis=1)
        match_up = pd.concat([match_up,name_series],axis=1)
        match_up = match_up.fillna(method='ffill').sort_values("Win rate",ascending=False)
        return match_up
    except:
        print("예외 상황")
        
def pick(color,position,champ):
    try:
        Target = "Blue"
        if color == "Blue":
            Target = "Red"
        team[f"{color}"].loc[f"{position}"] = champ
        if (pd.isnull(team[Target].loc[f"{position}"])) == False:
            data = match_up(f"{position}",team["Blue"].loc[f"{position}"])
            team["vs"].loc[f"{position}"] = float(data[data["Target"] == team["Red"].loc[f"{position}"]]["Win rate"])- 50
            if team.isnull().sum().sum() == 0:
                display(team)
            return

        else :
            if team.isnull().sum().sum() == 0:
                display(team)
            return
        
    except:
        print("예외 상황")
"""
예측 함수
: 입력한 소환사 명의 최근 전적 20게임 분석 
"""
def prediction(game_index):
    base_url = f"https://www.op.gg/summoners/kr/{summoners_name}"
    headers = {''}
    response = requests.get(base_url,headers=headers)
    html = bs(response.text,"lxml")
    c_list = html.select("#content-container > div.css-jpkp7v.e1shm8tx0 > ul > li > div")
    m_list = [c_list[game_index].select("div.participants > ul > li > div.icon > img")[index]["alt"] for index in range(10)]
    
    summoners_champ = c_list[game_index].select("div.info >div>div.champion > div.icon > a > img")[0]["alt"]
    summoners_color = "Blue"
    
    for where in range(10):
        if m_list[where] == summoners_champ:
            if where > 5 :
                summoners_color = "Red"
    
    
    pick("Blue","Top",m_list[0])
    pick("Blue","Jungle",m_list[1])
    pick("Blue","Mid",m_list[2])
    pick("Blue","Adc",m_list[3])
    pick("Blue","Support",m_list[4])
    pick("Red","Top",m_list[5])
    pick("Red","Jungle",m_list[6])
    pick("Red","Mid",m_list[7])
    pick("Red","Adc",m_list[8])
    pick("Red","Support",m_list[9])
    
    blue_win_rate = round(50 + team["vs"].sum(),2)
    red_win_rate = round(50 - team["vs"].sum(),2)
    game_result = c_list[game_index].select("div.result")[0].get_text()

    print("Blue Team Win rate : ", blue_win_rate)
    print("Red Team Win rate : " , red_win_rate)


    if (red_win_rate > blue_win_rate):
        print("승자 예측 : Red Team Win",end="\n\n")
    else :
        print("결과 예측 : Blue Team Win",end="\n\n")
    print(f"{name}({summoners_color}) 팀 결과 : ", game_result)
    
# 예측 시작
for count in range(20):
    team = pd.DataFrame(columns=["Blue","vs","Red"],index=["Top","Jungle","Mid","Adc","Support"]) 
    prediction(count)
