## 리그 오브 레전드 챔피언 조합별 승률 예측 및 픽 추천 시스템

### 실시간 게임 예측 진행, 예시
![Untitled](https://user-images.githubusercontent.com/105343823/174728242-10d15e70-6a3a-48aa-9dcf-1489d9575448.png)
![Untitled 1](https://user-images.githubusercontent.com/105343823/174728254-3c32d6be-8f19-44df-8bac-0a67d8b4ff2f.png)
![Untitled 2](https://user-images.githubusercontent.com/105343823/174728259-b32a3b20-ff17-4cba-84fd-0d74ff74cc64.png)


                                                                            🖥️

                                                                            🖥️

                                                                            🖥️

                                                                            🖥️

![Untitled 3](https://user-images.githubusercontent.com/105343823/174728489-c7d33d16-eda5-490a-a430-412ca2417a27.png)


---

## 실시간 예측

1. **2022-06-03 PM 10:00 스트리머 괴물쥐 승패 예측**
![Untitled 4](https://user-images.githubusercontent.com/105343823/174728398-fba16ff1-4e7a-4fea-8ab3-abce119020a7.png)

![Untitled 5](https://user-images.githubusercontent.com/105343823/174728359-da86aa67-3c4a-4bfe-af9c-b88a00aabaab.png)

![Untitled 6](https://user-images.githubusercontent.com/105343823/174733890-05036272-26d8-45a7-bcba-158eaf45af11.png)


**Red(괴물쥐) 팀, 패배 예측(49.21 : 50.79)**

**결과 : 48분 32초 접전 끝에 킬 스코어 27 : 35 Red(괴물쥐) 팀 패배**


## 최근 전적 20게임 예측

**2022-06-05 PM 6:00 스트리머 괴물쥐 전적 예측 및 결과**

![Untitled 7](https://user-images.githubusercontent.com/105343823/174733938-a8155b16-8421-4e81-b426-2cb3b964b2ef.png)

![Untitled 8](https://user-images.githubusercontent.com/105343823/174733960-b73051bf-1f52-4e61-908d-7987cefcf56b.png)

---

### 예측 결과 시각화 및 분석

```python
total = pd.DataFrame(columns=["예측 일치","예측 불일치","예측 불가"],index=["게임수"])

plt.figure(figsize=(12,6))
plt.xticks(fontsize=20)
plt.ylim(0,15)
plt.yticks(fontsize=20)
sns.barplot(data=total)
```

![save](https://user-images.githubusercontent.com/105343823/174734108-0fa7a594-aa9d-424a-a676-d220610a4675.png)


1. **소환사명**을 입력 받아 최근 전적 게임 예측 결과 또는 2. **수기로 라인별 챔피언**을 입력 받아

탑 62개 챔피언, 정글 45개 챔피언, 미드 57개 챔피언, 원딜 24개 챔피언, 서폿 46개 챔피언의 **오직 같은 라인의 챔피언 상성(승률)로 팀의 승패를 예측하는 코드**이다.  

op.gg의 챔피언 별 경우의 수를 최대한으로 늘리기 위해 티어는 **모든 티어의 통계**로 진행하였다.

 

트위치 스트리머 괴물쥐의 20건의 게임 결과를 표본으로 측정하였다.

**20건의 예측 중 예측 일치 13건, 예측 불일치 3건, 예측 불가 4건으로 65% 정도 예측하고 적중하였다.**

**예측 불가한 경우**는 해당 라인의 해당 챔피언 통계가 적은 경우이다. (ex 원딜 트린다미어, 원딜 그브)

드물게 **예측 승률이 50 : 50인 경우**에는 아래의 링크 통계를 참고하여 **블루** 팀의 승리로 예측하였다.

<aside>
💡 [https://www.leagueofgraphs.com/ko/rankings/blue-vs-red/kr/iron](https://www.leagueofgraphs.com/ko/rankings/blue-vs-red/kr/iron)

</aside>

**분석 과정**에서 흔히 말하는 **바텀 라인(원딜+서폿)**에 비해 **상체(탑+정글+미드)**가 수치상으로 게임에 영향을 크게 미치는 것을 볼 수 있었다. **바텀 라인**에 비해 **상체**가 인원이 많은 것 또한 이유지만 

**챔피언 상성별 승률 변동 폭**이 **바텀 포지션**에 비해 **상체 라인**에서 **넓은 걸 확인할 수 있었다**.

**솔로랭크 경기 전적**만 표본으로 삼았기에 **자유 랭크 또는 팀 게임에 능숙한 상위 티어**에서는 예측과 분석이 **불확실**하며 통계가 적은 챔피언 또한 다수 존재한다.

표본의 크기가 작고 리그 오브 레전드 게임의 다양한 변수 및 티어를 고려하지 않은 수치 이므로 

게임 진행 시 또는 관람 시 재미로 **참고하는 용도로 사용하면 좋을 것** 같다. 

**향후** 챔피언 별 플레이 시간 별 승률, 같은 팀원이 진행한 패치 버전별 승률 등 다양한 지표와 수치를 적용시켜 더욱 정확성 있는 승률 예측이 된다면 유용하게 사용할 수 있을 것 같다.


## 1. league_of_legend(region,tier,position)
### (지역, 티어, 포지션) 입력 시 해당 포지션 챔피언들의 상대 픽 추천(Top3) - 이름순

![image](https://user-images.githubusercontent.com/105343823/171563787-491938aa-da8e-4ca8-972b-8529f485985e.png)



## 2. recommend(position, champion)
### 포지션, 챔피언명 입력 시 해당 포지션 챔피언의 상대 픽 추천(Top3)

![image](https://user-images.githubusercontent.com/105343823/171564022-fbf21c6a-20ee-481e-a13b-84398faf8e3d.png)


## 3. all_list()
### 전 포지션 챔피언들의 상대 픽 추천(Top3) - 이름순

![image](https://user-images.githubusercontent.com/105343823/171564116-0a1a64fe-6a62-4b10-bac3-ca722e01b682.png)


## 4. match_up(position,champion)
### 입력한 포지션, 챔피언의 상대전적 - 승률순

![image](https://user-images.githubusercontent.com/105343823/171564170-8b29d325-34c4-45fa-8c01-fc88beebebb3.png)

