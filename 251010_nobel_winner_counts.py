import pandas as pd
from plotnine import (
    aes,
    element_text,
    facet_wrap,
    geom_line,
    ggplot,
    guide_legend,
    guides,
    labs,
    scale_y_continuous,
    theme,
)


class NobelData:
    def __init__(self, data):
        self.data = pd.DataFrame(data)

    def get_total_winners(self) -> int:
        self.total_winners = self.data['count'].sum()
        print('Total Nobel Laureates:', self.total_winners)
        return self.total_winners

    def get_total_winners_by_category(self) -> pd.Series:
        self.total_winners_by_category = self.data.groupby('category')['count'].sum()
        print('Total Nobel Laureates by Category:')
        print(self.total_winners_by_category)
        return self.total_winners_by_category

    def calc_mean_counts_per_decade_by_category(self):
        subset = self.data.copy()
        subset['decade'] = subset['year'] // 10 * 10

        # calculate mean of counts by decade and category
        mean_counts = (
            subset.groupby(['decade', 'category'])['count'].mean().reset_index()
        )
        return mean_counts

    def plot_counts_per_decade_by_category(self):
        mean_counts = self.calc_mean_counts_per_decade_by_category()
        plt = (
            ggplot(mean_counts, aes(x='decade', y='count', color='category'))
            + geom_line(size=1.5)
            + facet_wrap('category')
            + labs(x='Decade', y='# of Nobel laureates')
            + theme(
                axis_text_x=element_text(rotation=90, size=12),
                axis_text_y=element_text(size=12),
                strip_text=element_text(size=14),
                legend_text=element_text(size=12),
                legend_title=element_text(size=14),
            )
            + guides(color=guide_legend(title='Category'))
            + scale_y_continuous(breaks=[0, 1, 2, 3], limits=(0, 3))
        )
        plt.save(
            'plots/251010_nobel_laureate_counts_per_decade_by_category.png',
            dpi=300,
            width=10,
            height=6,
        )
        plt.show()


if __name__ == '__main__':
    data = pd.read_csv('data/nobel_prize_dataset.csv')
    nobel_data = NobelData(data)
    nobel_data.get_total_winners()
    nobel_data.get_total_winners_by_category()
    nobel_data.plot_counts_per_decade_by_category()
