import arviz as az
import bambi as bmb
import numpy as np
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
from plotnine import ggplot, aes, geom_density, geom_point, geom_histogram, scale_color_hue

az.style.use("arviz-darkgrid")


data = pd.read_csv('https://raw.githubusercontent.com/dustinstansbury/statistical-rethinking-2023/main/data/Howell1.csv', sep=';')
data

d2 = data.query("age >= 18")

model = bmb.Model(
    'height ~ 1',
    d2,
    priors={
        'Intercept':bmb.Prior('Normal', mu=178, sigma=20),
        'sigma': bmb.Prior('HalfNormal', sigma=5)
    },
    family="gaussian"
)
model
model.build()
model.plot_priors()
idata_prior = model.prior_predictive()
prior = az.extract(idata_prior, group="prior_predictive")["height"]
plt.clf()
plt.hist(prior)

results = model.fit(
    draws=1000, tune=1000, chains=4, cores=4,
    random_seed=4
)

az.plot_trace(results, compact=False)
az.summary(results)


# Add in weight

model = bmb.Model(
    "height ~ 1 + weight",
    d2,
    priors={
        "Intercept": bmb.Prior("Normal", mu=156, sigma=100),
        "weight": bmb.Prior("Normal", mu=0, sigma = 10),
        "sigma": bmb.Prior("Cauchy", alpha=0, beta=1),
    },
    family="gaussian",
)
model.build()
model.plot_priors()


results = model.fit(
    chains=4, cores=4, random_seed=4
)
az.plot_trace(results, compact=False)
az.summary(results)

samples = results.posterior
samples

sigmas = pd.DataFrame(samples["sigma"].values.flatten())
sigmas.columns = ['sigma']
(
    ggplot(sigmas)
    + geom_density(aes(x="sigma"))
)


params = list(samples.data_vars) # ['Intercept', 'sigma', 'weight']
params

def extract_param(param):
    return param.values.flatten()

def param_dataframe(samples):
    params = list(samples.data_vars)  # ['Intercept', 'sigma', 'weight']

    return pd.DataFrame({param: extract_param(samples[param]) for param in params})

df_params = param_dataframe(samples)
df_params

weights = np.arange(25, 75, 1)

df_posterior_pred = (
    pd.DataFrame({'weight': weights})
    .merge(df_params, how ='cross')
    .assign(pred = lambda x: x.Intercept + (x.weight_x*x.weight_y) + x.sigma)
)

# The posterior predictive regression lines
(
    ggplot(df_posterior_pred)
    + geom_point(aes("weight_x", "pred"))
)

preds = np.random.normal(
    df_posterior_pred['Intercept'] + (df_posterior_pred['weight_x']*df_posterior_pred['weight_y']),
    df_posterior_pred['sigma']

)

df_posterior_pred['sample_pred'] = preds
# This is the full posterior predictive distirbution
(ggplot(df_posterior_pred) + geom_point(aes("weight_x", "sample_pred")))


## Posterior Predictive built in functions

model.predict(results, kind="response")

az.plot_ppc(results)


## Add in sex

model = bmb.Model("height ~ 1 + bs(weight, df=3)",
    d2,
    priors={
        "Intercept": bmb.Prior("Normal", mu=156, sigma=100),
        "weight": bmb.Prior("Normal", mu=0, sigma=10),
        "sigma": bmb.Prior("Cauchy", alpha=0, beta=1)
    },
    family="gaussian",
)
model
model.build()
model.plot_priors()

results = model.fit(chains=4, cores=4, random_seed=4)
az.plot_trace(results, compact=False)
az.summary(results)
model.predict(results, kind='response')
az.plot_ppc(results, num_pp_samples=10)
