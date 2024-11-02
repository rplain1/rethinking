import arviz as az
import bambi as bmb
import numpy as np
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
from plotnine import ggplot, aes, geom_density, geom_point, geom_histogram, scale_color_hue

az.style.use("arviz-darkgrid")


data = pd.read_csv('https://raw.githubusercontent.com/dustinstansbury/statistical-rethinking-2023/main/data/WaffleDivorce.csv', sep=';')
data

data['D'] = (data['Divorce'] - data['Divorce'].std()) / data['Divorce'].std()
data["A"] = (data["MedianAgeMarriage"] - data["MedianAgeMarriage"].std()) / data[
    "MedianAgeMarriage"
].std()

model = bmb.Model(
    "D ~ 1 + A",
    priors={
        "Intercept": bmb.Prior("Normal", mu=0, sigma=0.2),
        "A": bmb.Prior("Normal", mu=0, sigma=0.5),
        "sigma": bmb.Prior("Exponential", lam=1),
    },
    data=data,
)
model.build()
model.plot_priors()
idata_prior = model.prior_predictive()
prior = az.extract(idata_prior, group="prior_predictive")["D"]
plt.clf()
plt.hist(prior)


results = model.fit(draws=1000, tune=1000, chains=4, cores=4, random_seed=4)

az.plot_trace(results, compact=False)
az.summary(results)


model = bmb.Model(
    "Divorce ~ 1 + MedianAgeMarriage",
    priors={
        "Intercept": bmb.Prior("Normal", mu=0, sigma=0.2),
        "MedianAgeMarriageA": bmb.Prior("Normal", mu=0, sigma=0.5),
        "sigma": bmb.Prior("Exponential", lam=1),
    },
    data=data,
)



results = model.fit(draws=1000, tune=1000, chains=4, cores=4, random_seed=4)

az.plot_trace(results, compact=False)
az.summary(results)
