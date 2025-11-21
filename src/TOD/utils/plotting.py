import pandas as pd
import pyam
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class Plotting:

    def __init__(self):
        self.scenario_colors = {
            "REF": "black",
            "LIFE-TP": "orange",
            "TECH-TP": "magenta",
            "REF-v2": "black",
            "LIFE-TP-v2": "orange",
            "TECH-TP-v2": "magenta",
        }

        self.regions_dict = {
            "Africa (UN-R5)": "Africa",
            "Asia and the Pacific (UN-R5)": "AatP",
            "Eastern Europe (UN-R5)": "EE",
            "Latin America and Caribbean (UN-R5)": "LaaC",
            "Western Europe and Other States (UN-R5)": "WeoS",
        }

    def plot_data_individual_figures(
        df,
        save_figures=False,
        variables=None,
    ):
        # Define the color palette for scenarios
        scenario_colors = {
            "REF": "black",
            "LIFE-TP": "orange",
            "TECH-TP": "magenta",
            "REF-v2": "black",
            "LIFE-TP-v2": "orange",
            "TECH-TP-v2": "magenta",
        }

        regions_dict = {
            "Africa (UN-R5)": "Africa",
            "Asia and the Pacific (UN-R5)": "AatP",
            "Eastern Europe (UN-R5)": "EE",
            "Latin America and Caribbean (UN-R5)": "LaaC",
            "Western Europe and Other States (UN-R5)": "WeoS",
        }

        if variables is None:
            variables = df.variable

        for region in list(regions_dict.keys()):
            df_plotting = (
                df.filter(
                    year=[2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050],
                    region=region,
                )
                .timeseries()
                .reset_index()
            )

            df_selected = df_plotting[df_plotting["variable"].isin(variables)]

            df_compare_data = pd.melt(
                df_selected,
                id_vars=["model", "scenario", "region", "variable", "unit"],
                var_name="year",
                value_name="value",
            )
            df_compare_data["year"] = df_compare_data["year"].astype(int)

            for variable in variables:
                # print(variable)
                # Use Seaborn to create the plot with markers and lines
                data = df_compare_data[df_compare_data["variable"] == variable]

                fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size
                sns.lineplot(
                    data=data,
                    x="year",
                    y="value",
                    hue="scenario",
                    # style="model",
                    dashes=True,
                    palette=scenario_colors,
                )

                # Set labels and title
                plt.xlabel("Year")
                plt.ylabel(data["unit"].iloc[0])  # Set the y-axis label to the unit
                # Set y-axis lower limit to 0
                ax.set_ylim(min(0, ax.get_ylim()[0]), ax.get_ylim()[1])
                # Set title
                fig.suptitle(f"{variable} \n {region}", fontsize=16)
                # Show legend and grid
                plt.legend(title="Legend", bbox_to_anchor=(1.3, 1))
                plt.grid(True)
                # Adjust layout to ensure legend fits within the saved image
                plt.tight_layout()

                if save_figures:
                    standard_path = "../../../plots/SOD/chpt_20/Regional/"
                    model_path = data.model.iloc[0]
                    variable_name = (
                        variable.replace(" > 25 μg/m3", "")
                        .replace("|", "_")
                        .replace(" ", "_")
                        .replace("/", "")
                    )

                    plt.savefig(
                        f"{standard_path}{regions_dict[region]}/{model_path}/{variable_name}.png"
                    )
                    plt.close()

    def plot_data_3_x_3_figures(
        self,
        df,
        title_dict=None,
        path_dict=None,
        variables=None,
    ):
        # Define the color palette for scenarios
        scenario_colors = self.scenario_colors

        df_plotting = (
            df.filter(year=[2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050])
            .timeseries()
            .reset_index()
        )
        df_compare_data = pd.melt(
            df_plotting,
            id_vars=["model", "scenario", "region", "variable", "unit"],
            var_name="year",
            value_name="value",
        )
        df_compare_data["year"] = df_compare_data["year"].astype(int)

        if variables is None:
            variables = df.variable

        for variable in variables:
            df_var = df_compare_data[df_compare_data["variable"] == variable]
            # Get unique regions for creating subplots
            unique_regions = df_var["region"].unique()

            # Create subplots based on the number of unique regions
            fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))

            # Initialize lists to store handles and labels for the legend
            legend_handles = []
            legend_labels = []

            # Iterate through each region and plot in respective subplot
            for idx, region in enumerate(unique_regions):
                row_idx = idx // 3
                col_idx = idx % 3

                ax = axes[row_idx, col_idx]  # Select the current subplot

                region_data = df_var[
                    df_var["region"] == region
                ]  # Filter data for the current region

                # Plot lineplots for each region
                lineplot = sns.lineplot(
                    data=region_data,
                    x="year",
                    y="value",
                    hue="scenario",
                    # style='model',
                    palette=scenario_colors,
                    linewidth=2.5,
                    ax=ax,
                )

                # Customize ticks and labels for the current subplot
                ax.set_ylabel(
                    region_data["unit"].iloc[0], fontsize=14
                )  # Set the y-axis label to the unit
                # Set y-axis lower limit to 0
                ax.set_ylim(min(0, ax.get_ylim()[0]), ax.get_ylim()[1])
                ax.set_xlabel("", fontsize=1)
                ax.set_title(f"{region}", fontsize=14)  # Set the title to the region
                ax.set_xticks([2010, 2020, 2030, 2040, 2050])
                ax.set_xticklabels(
                    [2010, 2020, 2030, 2040, 2050], rotation=45, fontsize=14
                )

                # Increase fontsize of y-axis tick labels
                ax.tick_params(axis="y", labelsize=14)

                # Add the lineplot to the legend manually
                legend_handles.append(lineplot)
                legend_labels.append(region)
                # Disable the legend for individual subplots
                ax.legend().set_visible(False)
                ax.grid(True)

                # Add a gray background for the 'World' region subplot
                if region == "World":
                    ax.set_facecolor(color="#ededed")

            # Show legend and grid for the current subplot
            if title_dict:
                fig.suptitle(f"{title_dict[variable]}", fontsize=16)
            else:
                fig.suptitle(variable, fontsize=16)

            handles, labels = ax.get_legend_handles_labels()
            fig.legend(handles, labels, title="Legend", bbox_to_anchor=(1.12, 0.55))
            plt.tight_layout()  # Adjust subplots to prevent overlap

            if path_dict:
                root_variable = variable.split("|")[0].replace(" ", "_")
                variable_name = (
                    variable.replace(" > 25 μg/m3", "")
                    .replace("|", "_")
                    .replace(" ", "_")
                    .replace("/", "")
                )
                plt.savefig(
                    f"../../../plots/SOD/chpt_20/Regional/{path_dict[variable]}/{variable_name}.png",
                    bbox_inches="tight",
                )
                plt.close()


if __name__ == "__main__":
    df_plot_test = pd.read_excel(
        "./././data/SOD/model_results/to_share/model_results_to_share.xlsx",
        sheet_name="data",
    )
    df_plot_test = df_plot_test.rename(columns={"subject": "model"})
    df_plot_test = pyam.IamDataFrame(df_plot_test)
    df_plot_test = df_plot_test.filter(variable="Population")
    Plotting.plot_data_3_x_3_figures(df=df_plot_test)
