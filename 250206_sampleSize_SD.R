# function to calculate std. dev. for multiple sample sizes
calc_n_sds <- function(dist = NULL, sample_size) {
   purrr::map_df(
      .x = sample_size, 
      .f = ~ return(data.frame(n = .x, 
                               sd = sd(sample(dist, .x, T)),
                               se = sd(sample(dist, .x, T)) / sqrt(.x))
                    )
   )
}

# simulate different distributions
set.seed(129)
n_dist <- rnorm(10000, 0, 1)

# calculate std. dev. for range of sample sizes
n_sds <- calc_n_sds(dist = n_dist, sample_size = seq(50, 7000, 100))

# plot distribution
hist(n_dist, 
     breaks = 100, 
     probability = T, 
     xlab = "mean = 0, std. dev. = 1",
     main = "Normal distribution (N = 10,000)",
     ylab = NULL,
     cex.main = 3, cex.lab = 1.75)
title(ylab = "Density", cex.lab = 1.75, line = 2.25)

# plot std. dev. estimation vs. sample size
png(filename = "plots/250206_sampleSize_SD.png",
    width = 866, height = 570)
plot(n_sds$n, n_sds$sd, 
     ylim = c(0, max(n_sds$sd)),
     col = "blue",
     type = "o",
     xlab = "Sample size",
     ylab = "", 
     main = "Standard deviation vs. sample size",
     cex.lab = 1.75, cex.main = 3, cex.axis = 1.5, 
     frame.plot = F)
title(ylab = "Estimate of std. dev.", cex.lab = 1.5, line = 2.5)

# true std. dev. line
abline(h = 1, lty = 2, col = "red")

# plot legend
legend(x = 4000, y = 0.4, 
       legend = c("Estimated std. dev.", "True std. dev."),
       col = c("blue", "red"),
       pch = c(1, NA),
       lty = c(1, 2),
       cex = 1.25)
dev.off()
