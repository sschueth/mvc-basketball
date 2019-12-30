## mvc-basketball
Machine learning project attempting to predict the outcome of Missouri Valley Conference basketball games

This project will use a neural network trained with supervised learning. The key factors to be used in this project come from Dean Oliver's "Four Factors of Success in Basetball".
[link to basketball-reference] (https://www.basketball-reference.com/about/factors.html)

Inputs:
* Home Team Shooting (for & against)
* Home Team Turnovers (for & against)
* Home Team Free Throws (for & against)
* Home Team Offensive Rebounds (for & against)
* Home Team Total Points (for & against)
* Away Team Shooting (for & against)
* Away Team Turnovers (for & against)
* Away Team Free Throws (for & against)
* Away Team Offensive Rebounds (for & against)
* Away Team Total Points (for & against)

Outputs: 
* Spread (Home team perspective)
* Moneyline (Confidence 0 to 1 the Home team wins)
* O/U (Total Points in Game)

![alt text](https://www.tutorialspoint.com/artificial_neural_network/images/supervised_learning.jpg "NN with Supervised Learning")


Steps to Update:
1. Get the latest box scores from this year.
	* Run money_valley_conference_scraper.py
	* Run money_valley_conference_parser.py
2. Create NN inputs/outputs from latest box scores.
	* Run mvc_create_nn_data.py
3. Re-train the NN with latest data set.
	* Run mvc_nn_mlp_regression.py
