library(rethinking)
data(WaffleDivorce)
d <- WaffleDivorce

rm(WaffleDivorce)
detach(package:rethinking, unload = T)
library(brms)
library(tidyverse)

head(d)
glimpse(d)


standardize_waffle_divorce <- function(df) {
  df |>
    dplyr::mutate(
      Marriage_s = rethinking::standardize(Marriage),
      Divorce_s = rethinking::standardize(Divorce),
      MedianAgeMarriage_s = rethinking::standardize(MedianAgeMarriage)
    ) |>
    tibble::as_tibble()
}


generate_new_data <- function(col_name) {
  tibble({{ col_name }} := seq(from = -3, to = 3.5, length.out = 30))
}

plot_fitted_data <- function(x = NULL, y = NULL) {
  # plot
  ggplot(
    data = f,
    aes(x = x, y = y)
  ) +
    geom_smooth(aes(ymin = Q2.5, ymax = Q97.5),
      stat = "identity",
      fill = "firebrick", color = "firebrick4", alpha = 1 / 5, size = 1 / 4
    ) +
    geom_point(
      data = d,
      aes(y = Divorce),
      size = 2, color = "firebrick4"
    ) +
    ylab("Divorce") +
    coord_cartesian(
      xlim = range(d$MedianAgeMarriage_s),
      ylim = range(d$Divorce)
    ) +
    theme_bw() +
    theme(panel.grid = element_blank())

}

d <- standardize_waffle_divorce(d)

b5.1 <-
  brm(
    data = d, family = gaussian,
    Divorce_s ~ 1 + MedianAgeMarriage_s,
    prior = c(
      prior(normal(10, 10), class = Intercept),
      prior(normal(0, 1), class = b),
      prior(uniform(0, 10), class = sigma)
    ),
    iter = 2000, warmup = 500, chains = 4, cores = 4,
    seed = 5
  )


# define the range of `MedianAgeMarriage_s` values we'd like to feed into `fitted()`
nd <- generate_new_data('MedianAgeMarriage_s')

# now use `fitted()` to get the model-implied trajectories
f <-
  fitted(b5.1, newdata = nd) %>%
  as_tibble() %>%
  # tack the `nd` data onto the `fitted()` results
  bind_cols(nd)

# plot
ggplot(
  data = f,
  aes(x = MedianAgeMarriage_s, y = Estimate)
) +
  geom_smooth(aes(ymin = Q2.5, ymax = Q97.5),
    stat = "identity",
    fill = "firebrick", color = "firebrick4", alpha = 1 / 5, size = 1 / 4
  ) +
  geom_point(
    data = d,
    aes(y = Divorce_s),
    size = 2, color = "firebrick4"
  ) +
  ylab("Divorce") +
  coord_cartesian(
    xlim = range(d$MedianAgeMarriage_s),
    ylim = range(d$Divorce_s)
  ) +
  theme_bw() +
  theme(panel.grid = element_blank())




## b5.2 prior predictive

b5.2 <-
  brm(
    data = d, family = gaussian,
    Divorce_s ~ 1 + Marriage_s,
    prior = c(
      prior(normal(0, 0.2), class = Intercept),
      prior(normal(0, 0.5), class = b),
      prior(exponential(1), class = sigma)
    ),
    iter = 2000, warmup = 500, chains = 4, cores = 4,
    seed = 5,
    sample_prior = "only"
  )

nd <- generate_new_data('Marriage_s')

f <-
  fitted(b5.2, newdata = nd) %>%
  as_tibble() %>%
  bind_cols(nd)

ggplot(
  data = f,
  aes(x = Marriage_s, y = Estimate)
) +
  geom_smooth(aes(ymin = Q2.5, ymax = Q97.5),
    stat = "identity",
    fill = "firebrick", color = "firebrick4", alpha = 1 / 5, size = 1 / 4
  ) +
  geom_point(
    data = d,
    aes(y = Divorce_s),
    size = 2, color = "firebrick4"
  ) +
  coord_cartesian(
    xlim = range(d$Marriage_s),
    ylim = range(d$Divorce_s)
  ) +
  ylab("Divorce") +
  theme_bw() +
  theme(panel.grid = element_blank())



## b5.2

b5.2 <-
  brm(
    data = d, family = gaussian,
    Divorce_s ~ 1 + Marriage_s,
    prior = c(
      prior(normal(0, 0.2), class = Intercept),
      prior(normal(0, 0.5), class = b),
      prior(exponential(1), class = sigma)
    ),
    iter = 2000, warmup = 500, chains = 4, cores = 4,
    seed = 5
  )

nd <- generate_new_data("Marriage_s")

f <-
  fitted(b5.2, newdata = nd) %>%
  as_tibble() %>%
  bind_cols(nd)

ggplot(
  data = f,
  aes(x = Marriage_s, y = Estimate)
) +
  geom_smooth(aes(ymin = Q2.5, ymax = Q97.5),
    stat = "identity",
    fill = "firebrick", color = "firebrick4", alpha = 1 / 5, size = 1 / 4
  ) +
  geom_point(
    data = d,
    aes(y = Divorce_s),
    size = 2, color = "firebrick4"
  ) +
  coord_cartesian(
    xlim = range(d$Marriage_s),
    ylim = range(d$Divorce_s)
  ) +
  ylab("Divorce") +
  theme_bw() +
  theme(panel.grid = element_blank())

"
Divorce rate is associated with both marriage rate and median age of marriage.
There is a positive association with marriage rate and a negative association
with median rate of marriage

5.1 tells us the _total_ influence of age at marriage is negatively associated. That includes
the indirect path from age -> marriage rate -> divorce rate

Age has an influence on both marriage rate and divorce rate
A --> M
A --> D
M --> D
"
