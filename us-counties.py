import pandas as pd
import numpy as np
import git
import os
import matplotlib.pyplot as plt

g = git.cmd.Git(os.getcwd())
g.fetch('upstream')
g.merge('upstream/master')
g.push('origin')

cases_by_county = pd.read_csv('us-counties.csv')

counties = {
    'Broward': 12011
    # 'Broward': 12011,
    # 'Essex' : 34013,
    # 'Nassau' : 36059,
    # 'Miami-Dade': 12086,
    # 'Palm Beach': 12099,
    # 'Harris': 48201
}

for i, (county_name, county_id) in enumerate(counties.items()):
    cases_in_county = cases_by_county.loc[cases_by_county['fips'] == county_id].sort_values('date')
    cases_in_county = cases_in_county.drop(axis=1, columns=['county', 'state', 'fips', 'deaths'])
    cases = cases_in_county['cases'].to_numpy()
    old_cases = np.concatenate(([0], cases[0:cases.size-1]))
    new_cases = cases - old_cases
    total_cases = np.cumsum(new_cases)
    offset = np.concatenate((np.zeros(7, dtype=int), total_cases[0:cases.size-7]))
    average_7 = (total_cases - offset) / 7 # Not technically correct for the first 6 days
    index = cases_in_county['date'].to_numpy()
    cases_in_county['new'] = new_cases
    cases_in_county['average_7'] = average_7
    plt.subplot(len(counties), 1, i + 1)
    plt.title(county_name)
    plt.bar(index, new_cases)
    plt.plot(index, average_7, 'r')
    print(cases_in_county.to_string(index=False))

plt.show()
