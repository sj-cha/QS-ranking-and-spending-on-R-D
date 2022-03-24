import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

qs = pd.read_csv("QS world university ranking.csv")
qs = qs[(qs["year"] == 2022) & (qs["rank_display"].str.contains("-") == False)].reset_index()
#Selecting universities in top 500 only
qs = qs[qs["rank_display"].astype(int) <= 500][["university", "score", "country"]]

world = pd.read_csv("List of countries by research and development spending.csv")
world.rename(columns = {"Country/Region": "country"}, inplace = True)
world.drop(world.columns[[0, 2, 6]], axis = 1, inplace = True)

qs["country"].replace({"China (Mainland)": "China", "Hong Kong SAR": "Hong Kong"}, inplace = True)

number_of_uni = qs.groupby("country").size().reset_index()
qs = qs.groupby("country").mean().reset_index()


#merging dataframes
joined_data = qs.merge(world, how = 'inner', on = 'country').merge(number_of_uni, how = 'inner', on = 'country')
joined_data.columns = ["Country", "Score", "% of GDP (PPP)", "Spending per capita (US$, PPP)", "Year", "Number of Universities"]
joined_data["Spending per capita (US$, PPP)"] = joined_data["Spending per capita (US$, PPP)"].str.replace("," , "").astype(int)
joined_data.sort_values(by = "Number of Universities", ascending = False, inplace = True)


#plots
fig, axes = plt.subplots(1, 2, figsize = (17, 7))
fig.suptitle("Does more spending on R&D result in higher score on QS Ranking?", fontsize = 18)

ax1 = axes[0].scatter(joined_data["% of GDP (PPP)"], joined_data["Score"], alpha = 0.7, s = 60*joined_data["Number of Universities"], c = joined_data["Number of Universities"], cmap='viridis_r')
ax2 = axes[1].scatter(joined_data["Spending per capita (US$, PPP)"], joined_data["Score"], alpha = 0.7, s = 60*joined_data["Number of Universities"],  c = joined_data["Number of Universities"], cmap='viridis_r')
axes[0].set_xlabel("% of GDP (PPP)", fontsize = 15, labelpad = 15)
axes[0].set_ylabel("Score", fontsize = 15, labelpad = 15)
axes[1].set_xlabel("per capita (US$, PPP)", fontsize = 15, labelpad = 15)

cax = fig.add_axes([0.93,0,0.02,0.88])
fig.colorbar(ax2, cax = cax).set_label("no. of universities in top 500", fontsize = 15, labelpad = 15)

axes[0].tick_params(labelsize = 12)
axes[1].tick_params(labelsize = 12)

axes[0].set_ylim([0, 100])
axes[1].set_ylim([0, 100])
axes[1].set_xlim([-100, 2100])

#ploting line of best fit 
from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(joined_data["% of GDP (PPP)"], joined_data["Score"])
line = slope * joined_data["% of GDP (PPP)"] + intercept
axes[0].plot(joined_data["% of GDP (PPP)"], line, "--k", alpha = 0.3, linewidth = 1.0)
axes[0].text(4.2, 55, "R = %s " %round(r_value, 5))

slope, intercept, r_value, p_value, std_err = stats.linregress(joined_data["Spending per capita (US$, PPP)"], joined_data["Score"])
line = slope * joined_data["Spending per capita (US$, PPP)"] + intercept
axes[1].plot(joined_data["Spending per capita (US$, PPP)"], line, "--k", alpha = 0.3, linewidth = 1.0)
axes[1].text(1700, 65, "R = %s " %round(r_value, 5))

