def returnIndex(countryName,country_names):
    i = 0
    for country in country_names:
        if country == countryName:
            return i
        else:
            i += 1
    return -1


def returnIndexlist(countryName,countries):
    lst = []
    for i in range(len(countries)):
        if countries[i] == countryName:
            lst.append(i)
    return lst


def mySortDescending(unSortedList):
    index_lst = []
    for i in range(len(unSortedList)):
        index_lst.append([unSortedList[i], i])
    index_lst.sort(reverse=True)
    sort_index = []
    for x in index_lst:
        sort_index.append(x[1])
    return sort_index


import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('Gapminder.csv')
countries = list(df.loc[:, 'Country'])
country_names = sorted(list(set(countries)))
Years = list(set(df.loc[:, 'Year']))
columnNames = list(df.head(0))


# Indexes or row numbers of all countries corresponding to the 'country_names' list.
country_indexes = []
for n in country_names:
    country_indexes.append((returnIndexlist(n, countries)))


# Cleaning Data. Replacing the missing values in each column by the column average.
for column in columnNames[6:len(columnNames)]:
    columnIndex = returnIndex(column, columnNames)
    unclean_data = df.iloc[:, columnIndex]
    avg_ = unclean_data.mean()
    df.iloc[:, columnIndex] = df.iloc[:, columnIndex].fillna(value=avg_)
    clean_data = df.iloc[:, columnIndex]


# Normalizing Data. Dividing all columns' values by the columns' max.
for column in columnNames[6:len(columnNames)]:
    df[column] = df[column]/df[column].max()


pillars = ['Technology', 'Environment', 'Economic', 'Social', 'Population', 'Health']
ele_list = [['Cellphones', 'Hightotechnologyexports', 'YearlyCO2emission'], ['AgriculturalLand', 'Forestarea', 'Renewablewater'], ['EnergyUsePerPerson', 'GDPpercapita', 'Hourlycompensation', 'IncomePerPerson', 'Inflation', 'Longtermunemploymentrate', 'Poverty', 'Taxrevenue', 'Tradebalance'], ['DemocracyScore', 'Literacyrateyouthtotal', 'Ratioofgirlstoboysinprimaryandsecondaryeducation', 'Murder'], ['Populationgrowth', 'Populationtotal'], ['LifeExpectancy', 'MedicalDoctors', 'TotalhealthspendingperpersonUS']]

# Finding averages of all indicators for every country.
AvgList = []
for ele in ele_list:
    for e in ele:
        for countryName in country_names:
            country_index = returnIndex(countryName, country_names)
            columnIndex = returnIndex(e, columnNames)
            countryData = df.iloc[country_indexes[country_index], columnIndex]
            avg_ = sum(countryData) / len(Years)
            AvgList.append(avg_)

# Grouping averages into lists of length 227.
length = 0
for to_sep in ele_list:
    length += len(to_sep)

i = 227
count = 0
AvgList2 = []
for c in range(0, length):
    AvgList2.append(list(AvgList[count:i]))
    count = i
    i += 227

# Making five sublists into one list containing indicators' averages for every pillar.
sep_avg = []
x = 0
for r in range(len(ele_list)):
    sep_avg.append(AvgList2[0:len(ele_list[x])])
    x += 1

# Weighted averages.
sep_avg2 = []
pillar_weight = []
weight_lst = [1/len(sep_avg[0]), 1/len(sep_avg[1]), 1/len(sep_avg[2]), 1/len(sep_avg[3]), 1/len(sep_avg[4]), 1/len(sep_avg[5])]

for sep in range(len(sep_avg)):
    for s in sep_avg[sep]:
        pillar_weight.append([w * weight_lst[sep] for w in s])
    sep_avg2.append(pillar_weight)
    pillar_weight = []

# Economy based model.
# Determining impact of indicators based on indicators' correlation with the Total GDP US.
pos_ele = ['Cellphones', 'Hightotechnologyexports', 'YearlyCO2emission', 'AgriculturalLand', 'Forestarea', 'EnergyUsePerPerson', 'GDPpercapita', 'Hourlycompensation', 'IncomePerPerson', 'Tradebalance', 'DemocracyScore', 'Literacyrateyouthtotal', 'Ratioofgirlstoboysinprimaryandsecondaryeducation', 'Populationtotal', 'LifeExpectancy', 'MedicalDoctors', 'TotalhealthspendingperpersonUS']
neg_ele = ['Inflation', 'Longtermunemploymentrate', 'Poverty', 'Murder', 'Taxrevenue', 'Populationgrowth', 'Renewablewater']


# Adding or subtracting averages based on their impact to get one average for every pillar.
all_agg = []
pillars = []
sum_avg = [0] * 227
for i in range(0, len(ele_list)):
    for a, b in zip(ele_list[i], sep_avg2[i]):
        if a in pos_ele:
            all_agg = [sum_avg[i] + b[i] for i in range(len(sum_avg))]
            sum_avg = all_agg
        elif a in neg_ele:
            all_agg = [b[i] - sum_avg[i] for i in range(len(sum_avg))]
            sum_avg = all_agg
    pillars.append(all_agg)
    all_agg = []

# Final Economy Ranking.
final_ranking = [pillars[0][i] + pillars[1][i] + pillars[2][i] + pillars[3][i] + pillars[4][i] + pillars[5][i] for i in range(len(country_names))]

sortedAvgIndices = mySortDescending(final_ranking)

# Top performing, under performing, and countries sharing near similar ranks to Pakistan.
CountriesForComparison = ['Uzbekistan', 'Western Sahara', 'Uruguay', 'United States of America', 'China', 'Japan', 'Germany', 'Norfolk', 'Pitcairn', 'Norway', 'Qatar', 'Pakistan', 'Burundi', 'Mongolia', 'India', 'Denmark', 'Czech Republic']

countries_lst = []
rank_lst = []
print("// \n Countries are ranked below based on their economy. \n Economic TESPH: \n //  ")
rank = 1
for index in sortedAvgIndices:
    print('At No. ', rank, ' is: ', country_names[index], 'with TESPH ranking of ', final_ranking[index])
    rank += 1
    if country_names[index] in CountriesForComparison:
        countries_lst.append(country_names[index])
        rank_lst.append(final_ranking[index])

# Graph showing final economy rankings of selected countries.
for r, a in zip(countries_lst, rank_lst):
    plt.bar(r, a)
plt.title('Economy TESPH Ranking')
plt.ylabel("Final Rankings")
plt.xlabel("Countries")
plt.xticks(rotation=90)
plt.show()


# Health and Environment based model.
# Determining impact of indicators based on indicators' correlation with Life Expectancy.
pos_ele2 = ['Hightotechnologyexports', 'EnergyUsePerPerson', 'GDPpercapita', 'Forestarea', 'Renewablewater', 'Hourlycompensation', 'IncomePerPerson', 'Taxrevenue', 'Tradebalance', 'DemocracyScore', 'Literacyrateyouthtotal', 'Ratioofgirlstoboysinprimaryandsecondaryeducation', 'LifeExpectancy', 'MedicalDoctors', 'TotalhealthspendingperpersonUS', 'Populationtotal', 'Cellphones']
neg_ele2 = ['Inflation', 'Longtermunemploymentrate', 'Poverty', 'AgriculturalLand', 'Murder', 'Populationgrowth', 'YearlyCO2emission']

all_agg2 = []
pillars2 = []
sum_avg2 = [0] * 227
for i in range(0, len(ele_list)):
    for a, b in zip(ele_list[i], sep_avg2[i]):
        if a in pos_ele2:
            all_agg2 = [sum_avg2[i] + b[i] for i in range(len(sum_avg2))]
            sum_avg2 = all_agg2
        elif a in neg_ele2:
            all_agg2 = [b[i] - sum_avg2[i] for i in range(len(sum_avg2))]
            sum_avg2 = all_agg2
    pillars2.append(all_agg2)
    all_agg2 = []

# Final Green Ranking.
final_ranking2 = [pillars2[0][i] + pillars2[1][i] + pillars2[2][i] + pillars2[3][i] + pillars2[4][i] + pillars2[5][i] for i in range(len(country_names))]

sortedAvgIndices2 = mySortDescending(final_ranking2)

countries_lst2 = []
rank_lst2 = []
print("// \n Countries are ranked below based on their health and environment. \n Green TESPH: \n //  ")
rank = 1
for index in sortedAvgIndices2:
    print('At No. ', rank, ' is: ', country_names[index], 'with TESPH ranking of ', final_ranking2[index])
    rank += 1
    if country_names[index] in CountriesForComparison:
        countries_lst2.append(country_names[index])
        rank_lst2.append(final_ranking2[index])

# Graph showing final green rankings of selected countries.
for r, a in zip(countries_lst2, rank_lst2):
    plt.bar(r, a)
plt.title('Green TESPH Ranking')
plt.ylabel("Final Rankings")
plt.xlabel("Countries")
plt.xticks(rotation=90)
plt.show()


# Bubble Graph of GDP per capita and Life Expectancy.
import plotly.express as px
fig = px.scatter(data_frame= df,
                 x='GDPpercapita', y='LifeExpectancy',
                 size='Populationtotal', hover_name='Country', color='Continent',
                 animation_frame='Year', animation_group='Country',
                 range_x=[-0.1,0.5], range_y=[0,2], size_max=90)
fig.show()

print(df.loc["GDPpercapita"])
