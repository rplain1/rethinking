data {
  int<lower=0> N;
  int<lower=0> features;
  matrix[N, features] X;
  vector[N] y;
}

parameters {
  real alpha;
  vector[features] beta;
  real<lower=0> sigma;
}

model {
  alpha ~ normal(0, 1);
  beta ~ normal(0, 1);
  sigma ~ exponential(1);

  y ~ normal(alpha + X * beta, sigma);
}

generated quantities {
  vector[N] y_rep;
  for (n in 1:N) {
    y_rep[n] = normal_rng(alpha + X[n] * beta, sigma);
  }
}
