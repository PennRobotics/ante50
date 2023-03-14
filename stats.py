import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns

sea_style = sns.axes_style()
sea_style['ytick.left'] = False
sea_style['xtick.bottom'] = False
sns.set_theme(style=sea_style)

class Strategy:
    def __init__(self):
        self.strength_table = [
                #A K Q J T 9 8 7 6 5 4 3 2 (suited)
                [8,8,7,7,6,4,4,4,4,4,4,4,4], # A
                [7,8,7,6,5,3,2,2,2,2,2,2,2], # K
                [6,5,8,6,5,4,2,0,0,0,0,0,0], # Q
                [5,4,4,8,6,5,3,1,0,0,0,0,0], # J
                [3,3,3,4,7,5,4,2,0,0,0,0,0], # T
                [1,1,1,2,2,6,5,4,1,0,0,0,0], # 9
                [0,0,0,1,1,2,5,4,3,1,0,0,0], # 8
                [0,0,0,0,0,0,1,4,4,3,1,0,0], # 7
                [0,0,0,0,0,0,0,1,3,2,2,0,0], # 6
                [0,0,0,0,0,0,0,0,1,3,3,2,0], # 5
                [0,0,0,0,0,0,0,0,0,1,2,2,1], # 4
                [0,0,0,0,0,0,0,0,0,0,0,2,1], # 3
                [0,0,0,0,0,0,0,0,0,0,0,0,2]] # 2
                # (off-suit)


strat = Strategy()

card_name_list = [s.replace('T','10') for s in 'AKQJT98765432']
preflop_strength_df = pd.DataFrame(strat.strength_table, columns=card_name_list, index=card_name_list)

f, ax = plt.subplots()
nplayers = 10
hmh = sns.heatmap(preflop_strength_df, annot=True, fmt='d', linewidths=.5, cmap='RdYlGn', ax=ax).set(title=f'Preflop Strength ({nplayers} players)')
#cmap = ListedColormap(["black", "darkred", "saddlebrown", "sienna", "darkgoldenrod", "darkkhaki", "yellowgreen", "limegreen", "lawngreen"])
#sns.heatmap(preflop_strength_df, annot=True, fmt='d', linewidths=.5, cbar=False, cmap=cmap, ax=ax)
plt.text(10.25, 4.5, "Suited", bbox=dict(boxstyle='ellipse', alpha=0.8, facecolor='#FFFFFF'))
plt.text(2.5, 11.25, "Off-suit", bbox=dict(boxstyle='ellipse', alpha=0.8, facecolor='#FFFFFF'))
plt.show()

