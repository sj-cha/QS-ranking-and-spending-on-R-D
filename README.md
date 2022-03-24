# QS ranking vs. Government's spending on research
Yes, not all of them are publicly funded, but most of them often get grants and funding from the government to do research. We know better performance in research matters in the global university ranking, like QS. Would higher spending on Research and Development (R&D) help universities performing better on ranking?


# Notes
* Only those nations which annually spend more than 50 million US dollars on R&D have been included, 
* Only universities in the Top 500 in 2022 are considered for calculation,

``` 
qs = qs[(qs["year"] == 2022) & (qs["rank_display"].str.contains("-") == False)].reset_index()
qs = qs[qs["rank_display"].astype(int) <= 500][["university", "score", "country"]]
```
* An average `Score` was taken for all universities in each country,
* The latest data for each country's spending varies and is indicated in the `Year` column.

# Conclusion 

![Result](https://raw.githubusercontent.com/sj-cha/QS-ranking-and-spending-on-R-D/main/QS%20ranking%20and%20spending%20on%20R%26D/plot.png)

By looking at the plot and the r-value, it seems like there exists a moderate positive correlation between the variables. Spending per capita proves to be a better indicator when it comes to predicting performancce on QS, and the r-value of 0.52 was higher than I've expected. 

**Note** : I accounted for the number of universities the country has in top 500 by varying a marker size. I thought it might be a little biased to not do so, because obviously having 87 universities in top 500 like US does takes more effort than say, Singapore, which only has two. 

# Source
List of countries by research and development spending: https://en.wikipedia.org/wiki/List_of_countries_by_research_and_development_spending

QS ranking data (2017-2022): https://www.kaggle.com/datasets/padhmam/qs-world-university-rankings-2017-2022
