import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

np.set_printoptions(legacy='1.25')

# simulate a random normal population (mean 167, sd 4)
rng = np.random.default_rng(12345)
pop = rng.normal(loc=167, scale=4, size=10000)

# initiate empty arrays to hold values
is_in_CI = np.array([])
n_exp = np.array([])
pct_exp_w_true_param = np.array([])

for _ in range(300):
    for _ in range(100):
        # choose two random samples
        sample1 = rng.choice(pop, size=100, replace=True)
        sample2 = rng.choice(pop, size=100, replace=True)
        ttest_res = stats.ttest_ind(sample1, sample2, equal_var=False)
        conf_int = ttest_res.confidence_interval(confidence_level=0.95)
        is_in_CI = np.append(is_in_CI, [min(conf_int) <= 0 <= max(conf_int)])
    n_exp = np.append(n_exp, is_in_CI.size)
    pct_exp_w_true_param = np.append(pct_exp_w_true_param, is_in_CI.sum() / is_in_CI.size)

# sanity check
print(f'{is_in_CI.sum()}')
print(max(n_exp))
print(pct_exp_w_true_param[-1])

fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-') # Initialize an empty line, 'r-' for red line
ax.axhline(y=0.95, color='lightgray', linestyle='--', zorder=0)

# set plot limits
ax.set_xlim(0, n_exp.max())
ax.set_ylim(pct_exp_w_true_param.min(), 1)

# set labels and title
ax.set_xlabel("# experiments")
ax.set_ylabel("% CIs containing true pop parameter")
ax.set_title("Visual representation of \n % CIs containing true parameter reaching the threshold")

# Add website text in the top right corner
website_text = "https://n.singh.phd"
ax.text(29000, 0.995, website_text, fontsize=10, color="gray", ha="right")

# animation update function
def update(frame):
    line.set_data(n_exp[:frame+1], pct_exp_w_true_param[:frame+1])
    return line,

# create
anim = FuncAnimation(fig, update, init_func=None, frames=len(n_exp), blit=True, repeat=False)

anim.save('plots/250612_CI-convergence.gif', writer='pillow', fps=30)
