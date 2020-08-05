# NBA Game Predictor

## Introduction

I have long wanted to create my own model to predict how the NBA season would resolve. With the break in the NBA season starting March 11th, I had an opportunity to create such a model. What follows is a description of how the model works, the decisions made along the way, and reflection on the process. 

## Construction

There were three components in the construction of the model: the data collection, the machine learning model training, and the simulation. Data was collected on each NBA game from the 2000-01 season until the break on March 11th of this year (2020). The data was then used to train a model to predict the winner of an NBA game. That model was then used to simulate 50000 instances of the remaining NBA regular season and playoffs. The model was developed entirely in Python, either locally on my machine or on Google Colab in the form of Python Notebooks. 

###  Data 

Data was derived from [Basketball Reference](https://www.basketball-reference.com). Each row has 4389 values:
-	Year
-	Month
-	Day
-	Home Team*
-	Away Team* 
-	Is Playoff Game (1 yes, 0 no)
-	For Both Home Then Away Teams:
    - Number of Games Played (including playoffs)
    - Win Percentage
    - Win Percentage at Home
    - Percent of Games Played at Home
    - Percent of Games Played with this Starting Five
    - Win Percentage with this Starting Five
    - Days of Rest (Days since last game, max 7) [divided by 7]**
-	For All Players***:
    - Weight
    - Height
    - Age
    - Percentage of Games Played with This Team This Season 
    - For Current and Previous Three Seasons and Three Postseasons:
        - Games Played
        - Games Started
        - Minutes per Game
        - Offensive Rebounds per Game
        - Defensive Rebounds per Game
        - Assists per Game
        - Blocks per Game
        - Steals per Game
        - Turnovers per Game
        - Personal Fouls per Game
        - Free Throw Attempts per Game
        - Free Throw Percentage
        - 3-point Attempts per Game
        - 3-point Percentage
    - For Previous Three Seasons and Postseasons only:
        - Attempts between 16 ft and 3-point line
        - Percentage between 16 ft and 3-point line
        - Attempts between 10ft and 16ft
        - Percentage between 10ft and 16ft
        - Attempts between 3ft and 10ft
        - Percentage between 3ft and 10ft
        - Attempts between 0ft and 3ft
        - Percentage between 0ft and 3ft
    - For Current Season and Postseason only:
        - 2-point Attempts per Game
        - 2-point Percentage
- Game Result (score of home team minus score of away team)

I tried to find a balance between what was available on basketball reference, and what could be useful for a model. I considered that previous seasons data would be helpful early on in the season, and that more than one could be useful in case of long term injury. I also considered that shot location would be important. Points per game is missing as this can be derived from attempts and field goal percentage from various shot locations.  

### Machine Learning Model

For the training of the model, I chose to exlude the identity of the home and away teams, as well as the date. I also changed the result from the point differential, to 1 or -1 depending on if the home team won. This changes the problem from regression, to binary classification. I made this decision because my true desire was to predict the chance that a team would win a game, which can be directly derived from a binary classifier. 

I ended up choosing XGBoost to train the model with. I chose it because it has a decent reputation and ended up performing fairly well. After some parameter tuning, I was able to correctly predict about 67% of NBA games in my validation set. 

### Simulation

After I had the model, simulation was fairly simple. Given a schedule and playoff structure, the simulation randomly selects winners for games depending on the percent chance of winning presented by the machine learning model. The team information is updated based on the result of each game. However, the player information is not. 

## Results

After running the simulation 50,000 times, these were the results for the 22 teams currently still in contention based on games played up through 8/2/2020:

Team | Make Playoffs | Make 2nd Round | Make Conf Finals | Make Finals | Win Finals |
--- | --- | --- | --- | --- | ---
HOU |100.0% | 90.6% | 69.5% |	54.6% |	37.4% |
TOR | 100.0% |	99.2% |	93.5% |	45.1% |	20.7% |
MIL | 100.0% |	99.6% |	70.0% |	44.1% |	20.5% |
LAC |100.0% |	99.2% |	60.7% |	34.1% |	15.2% |
DEN | 100.0% |	63.2% |	28.1% |	7.7% |	2.5% |
IND | 100.0% |	62.8% |	23.0% |	7.4% |	1.5% |
LAL | 100.0% |	78.8% |	27.6% |	2.1% |	1.0% |
PHI | 100.0% |	54.3% |	10.9% |	3.2% |	0.8% |
UTA | 100.0% |	31.0% |	7.1% |	0.9% |	0.3% |
POR | 24.8% |	6.6% |	2.0% |	0.2% |	0.0% |
SAS | 22.5% |	11.4% |	2.6% |	0.2% |	0.0% |
BOS | 100.0% |	60.3% |	0.7% |	0.1% |	0.0% |
OKC | 100.0% |	15.8% |	2.2% |	0.2% |	0.0% |
MIA | 100.0% |	22.7% |	1.7% |	0.1% |	0.0% |
ORL | 100.0% |	0.8% |	0.1% |	0.0% |	0.0% |
BRK | 100.0% |	0.4% |	0.0% |	0.0% |	0.0% |
DAL | 100.0% |	0.1% |	0.0% |	0.0% |	0.0% |
MEM | 40.7% |	1.3% |	0.1% |	0.0% |	0.0% |
NOP | 9.9% |	1.6% |	0.2% |	0.0% |	0.0% |
SAC | 1.6% |	0.2% |	0.0% |	0.0% |	0.0% |
PHO | 0.5% |	0.1% |	0.0% |	0.0% |	0.0% |
WAS | 0.0% |	0.0% |	0.0% |	0.0% |	0.0% |

I think it has some interesting insights, but also some areas where it seems just plain wrong. I think it is interesting that it thinks the Rockets are as strong of contenders as it does. It is also interesting how it seems to find the Spurs, Pacers, and Nuggets stronger than many believe. However, it is hard for me to believe that the Lakers are as weak as this model believes. Lastly though, I am glad that fringe teams are not dominating the model. 

## Reflection and Future Work

There are opportunities for future work and improvement. Originally, I had wanted to use a neural network. I think that a neural network would be able to handle the format of the data much better. It would also allow for data augmentation in the form of swtiching the order of players randomly. However, I was not able to configure a neural network to properly learn, most commonly it would fall back on guessing the same value for all games. This was true for all the learning rates and network structures I tried. I would probably need to take a very methodical approach to slowly arriving at a neural network that worked, but I currently do not have time for that. I look forward to doing it in the future.

The simulation process could also be built upon. This process lends itself to being displayed live. I could build a website with a UI to display predictions, refreshing the data and then predictions after each day. 

Lastly, the code is very messy. I should add documentationa and clean up the structure, getting rid of repeated code. However, I do think 