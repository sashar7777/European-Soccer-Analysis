import sqlite3
import datetime
import csv

print(datetime.datetime.now().time())
conn = sqlite3.connect(r'C:\Users\shyam.ashar\Desktop\soccer\database.sqlite')
c = conn.cursor()
c.execute("delete from Match_Ages")

c.execute("SELECT id,country_id,league_id,season,date,home_team_api_id,away_team_api_id,"\
          "home_player_1, home_player_2,home_player_3, home_player_4, home_player_5, home_player_6, home_player_7, home_player_8, home_player_9, home_player_10, home_player_11,"\
          "away_player_1, away_player_2, away_player_3, away_player_4, away_player_5, away_player_6, away_player_7, away_player_8, away_player_9, away_player_10, away_player_11 "\
          "from Match where season > '2011/2012'")

##
matches = c.fetchall()

c.execute('SELECT player_api_id,birthday FROM Player')

players = c.fetchall()

matches_with_player_ages = list()

for i in range(len(matches)):

    try:

        matches_with_player_ages.append(list(matches[i]))
        homeplayerages = datetime.timedelta()
        awayplayerages = datetime.timedelta()
        homeplayerwithnoage = 0
        awayplayerwithnoage = 0

    ## Home Team players age calculation as of date of match played
        
        for homeplayercount in range(7,18):

            age = datetime.timedelta(0)

            for homeplayer in players:

                if homeplayer[0] == matches[i][homeplayercount]:

                    age = datetime.datetime.strptime(matches[i][4],'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(homeplayer[1],'%Y-%m-%d %H:%M:%S')
                
            matches_with_player_ages[i].append(age)                                                                                                     
                    

            ##matches_with_player_ages[i].append([datetime.datetime.strptime(matches[i][4],'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(homeplayer[1],'%Y-%m-%d %H:%M:%S') for homeplayer in players if homeplayer[0] == matches[i][homeplayercount]])
            


    ## Away Team players age calculation as of date of match played

        for homeplayercount in range(18,29):

            age = datetime.timedelta(0)

            for homeplayer in players:

                if homeplayer[0] == matches[i][homeplayercount]:

                    age = datetime.datetime.strptime(matches[i][4],'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(homeplayer[1],'%Y-%m-%d %H:%M:%S')
                
            matches_with_player_ages[i].append(age)       
            
            ##matches_with_player_ages[i].append([datetime.datetime.strptime(matches[i][4],'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(homeplayer[1],'%Y-%m-%d %H:%M:%S') for homeplayer in players if homeplayer[0] == matches[i][homeplayercount]])
            
            
    ## Add colums for sum, max and min age of the team for a given match  


        ##print(matches_with_player_ages[29:40])
        matches_with_player_ages[i].append((sum([x for x in matches_with_player_ages[i][29:40]],datetime.timedelta())/sum(1 for x in matches_with_player_ages[i][29:40] if x != datetime.timedelta(0))).days/365)
        matches_with_player_ages[i].append((max(matches_with_player_ages[i][29:40])).days/365)
        matches_with_player_ages[i].append((min(x for x in matches_with_player_ages[i][29:40] if x != datetime.timedelta(0))).days/365)

        matches_with_player_ages[i].append((sum([x for x in matches_with_player_ages[i][40:51]],datetime.timedelta())/sum(1 for x in matches_with_player_ages[i][40:51] if x != datetime.timedelta(0))).days/365)
        matches_with_player_ages[i].append((max(matches_with_player_ages[i][40:51])).days/365)
        matches_with_player_ages[i].append((min(x for x in matches_with_player_ages[i][40:51] if x != datetime.timedelta(0))).days/365)


    except ValueError:

        print(i)
        continue

    except ZeroDivisionError:

        print(i)
        continue

##c.execute("Create table Match_Ages (id,country_id,league_id,season,date,team_api_id,team_avg_age,team_max_age,team_min_age)")

insert_matches = list()


for i in range(len(matches_with_player_ages)):

    insert_matches.append((matches_with_player_ages[i][0],matches_with_player_ages[i][1],matches_with_player_ages[i][2],matches_with_player_ages[i][3],matches_with_player_ages[i][4],matches_with_player_ages[i][5],matches_with_player_ages[i][51],matches_with_player_ages[i][52],matches_with_player_ages[i][53]))
    insert_matches.append((matches_with_player_ages[i][0],matches_with_player_ages[i][1],matches_with_player_ages[i][2],matches_with_player_ages[i][3],matches_with_player_ages[i][4],matches_with_player_ages[i][6],matches_with_player_ages[i][54],matches_with_player_ages[i][55],matches_with_player_ages[i][56]))

c.executemany("Insert into Match_Ages values (?,?,?,?,?,?,?,?,?)",insert_matches)
c.executemany("Insert into Match_Ages values (?,?,?,?,?,?,?,?,?)",insert_matches)

conn.commit()

c.execute("select league.name,team.team_long_name,match.* from Match_Ages match join league on match.country_id = league.country_id"\
          " join team on team.team_api_id = match.team_api_id")
           
##print matches_with_player_ages[6344]

with open('C:/Users/shyam.ashar/Desktop/soccer/matches_with_age_teams_league.csv', 'w') as csvfile:
    #outwriter = csv.writer(csvfile, delimiter=' ')

    for item in c.fetchall():
        csvfile.write(str(item) + '\n')
