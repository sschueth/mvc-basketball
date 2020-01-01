## mvc-basketball
Machine learning project attempting to predict the outcome of Missouri Valley Conference basketball games.

This project will use a neural network trained using supervised learning. The key factors to be used in this project come from Dean Oliver's "Four Factors of Success in Basetball" (listed below).
[link to basketball-reference] (https://www.basketball-reference.com/about/factors.html)

1. Shooting: eFG%
2. Ball Control: TOV%
3. Rebounding: ORB% & DRB%
4. Free Throws: FTf

### Moneyline NN
MLP Classifier Neural Network with two hidden layers consisting of 20 nuerons each using the logistic activation function outputting a predicted winner.

Inputs:
* Home Team Shooting (for)
* Home Team Ball Control (for)
* Home Team Rebounding (for)
* Home Team Free Throws (for)
* Home Team Shooting (against)
* Home Team Ball Control (against)
* Home Team Rebounding (against)
* Home Team Free Throws (against)
* Away Team Shooting (for)
* Away Team Ball Control (for)
* Away Team Rebounding (for)
* Away Team Free Throws (for)
* Away Team Shooting (against)
* Away Team Ball Control (against)
* Away Team Rebounding (against)
* Away Team Free Throws (against)

Outputs: 
* Log(Probability(Away Team Wins))
* Log(Probability(Home Team Wins))

Using just the "Four Factors of Success in Basketball" as my NN inputs I really struggled predicting the spread and o/u because all of the inputs are percentages. However, predicting the moneyline (winner) is quite successful. To obtain the ideal outputs (below), I believe I will need to include average points and possesions per game at the very minimum.
* Spread (Home team perspective)
* Moneyline (Confidence 0 to 1 the Home team wins)
* O/U (Total Points in Game)

![alt text](https://www.tutorialspoint.com/artificial_neural_network/images/supervised_learning.jpg "NN with Supervised Learning")



Scripts to run:
1. mvc_nightly_update.py
	* Make sure the database is fully updated with the latest games...
2. mvc_predict_games.py
	* Make predictions on the upcoming games...
