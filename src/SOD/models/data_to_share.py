import pandas as pd
import pyam
import numpy as np
import openpyxl


def round_to_0_1_percent(value):
    if value == 0:
        return 0
    # Determine the number of significant digits to round to
    magnitude = np.floor(np.log10(abs(value))) - 2
    rounding_factor = 10**magnitude
    return np.round(value / rounding_factor) * rounding_factor


def renaming(df):
    df.rename(
        scenario={"REF-v2": "REF", "TECH-TP-v2": "TECH-TP", "LIFE-TP-v2": "LIFE-TP"},
        inplace=True,
    )
    # IMAGE and AIM are already renamed in the processing of the results
    model_to_topic_map = {
        "GTEM-Resource_2023": "Materials_Circularity",
        "IFs 8.26": "Socio_Economics",
        "IMAGE-GLOBIO 3.3": "Biodiversity",
        "IMAGE-GNM 3.3": "Nutrient_Pollution",
        "JRC-FASST 1.0.0": "Air_Pollution",
        "MIMOSA": "Macro_Economy",
        "GEM-E3_V2023": "Macro_Economy",
    }

    df.rename(model=model_to_topic_map, inplace=True)


df_aim_image = pyam.IamDataFrame(
    "./././data/SOD/model_results/to_share/IMAGE_and_AIM_to_share.xlsx"
)
df_fasst = pyam.IamDataFrame(
    "./././data/SOD/model_results/to_share/FASST_to_share.xlsx"
)
df_ifs = pyam.IamDataFrame("./././data/SOD/model_results/to_share/IFs_to_share.xlsx")
df_globio = pyam.IamDataFrame(
    "./././data/SOD/model_results/to_share/GLOBIO_to_share.xlsx"
)
df_gnm = pyam.IamDataFrame("./././data/SOD/model_results/to_share/GNM_to_share.xlsx")
df_gtem = pyam.IamDataFrame("./././data/SOD/model_results/to_share/GTEM_to_share.xlsx")
df_mimosa = pyam.IamDataFrame(
    "./././data/SOD/model_results/to_share/MIMOSA_to_share.xlsx"
)
df_gem = pyam.IamDataFrame("./././data/SOD/model_results/to_share/GEM_E3_to_share.xlsx")

df_gdp = pyam.IamDataFrame("./././data/SOD/model_results/to_share/GDP_to_share.xlsx")

# Chapter 19 specific data
df_19 = pd.read_excel("./././data/SOD/model_results/to_share/Chapter_19_to_share.xlsx")
df_19_gdp = pd.read_excel(
    "./././data/SOD/model_results/to_share/GDP_to_share_chapter_19.xlsx"
)

df_list = [
    df_aim_image,
    df_fasst,
    df_ifs,
    df_globio,
    df_gnm,
    df_gtem,
    df_mimosa,
    df_gem,
    df_gdp,
]

for df in df_list:
    renaming(df)

df_to_share = pyam.concat(df_list)
df_to_share_19 = pd.concat([df_19, df_19_gdp]).reset_index(drop=True)

# In the Meta dataframe duplicates will exist, but we ignore those
# df_to_share = df_to_share.rename(model=model_to_topic_map, check_duplicates=False)
unique_vars = df_to_share.variable
df_to_share = (
    df_to_share.filter(year=[2000, 2010, 2020, 2030, 2040, 2050])
    .timeseries()
    .reset_index()
)

# All variables with unit % should be rounded to whole number except for specific variables
# Ugly double code
ratio_mask = (df_to_share["unit"].isin(["%", "% of GDP"])) & (
    ~df_to_share["variable"].isin(
        [
            "Damage Costs|Indirect",
            "Damage Costs|Relative",
            "GDP|Climate Damage Corrected|Loss|Relative",
            "Unemployment|Rate",
        ]
    )
)

df_to_share.loc[ratio_mask, df_to_share.columns[5:]] = round(
    df_to_share.loc[ratio_mask, df_to_share.columns[5:]]
)

ratio_mask_exception = df_to_share["variable"].isin(
    [
        "Damage Costs|Indirect",
        "Damage Costs|Relative",
        "GDP|Climate Damage Corrected|Loss|Relative",
        "Unemployment|Rate",
    ]
)

df_to_share.loc[ratio_mask_exception, df_to_share.columns[5:]] = round(
    df_to_share.loc[ratio_mask_exception, df_to_share.columns[5:]], 1
)

df_to_share.loc[:, df_to_share.columns[5:]] = df_to_share.loc[
    :, df_to_share.columns[5:]
].applymap(round_to_0_1_percent)

# df_to_share = df_to_share.rename(columns={"model": "subject"})
# Path to the existing Excel file
file_path = "./././data/SOD/model_results/to_share/model_results_to_share.xlsx"
file_path_19 = (
    "./././data/SOD/model_results/to_share/model_results_to_share_Chapter_19.xlsx"
)

df_to_share.to_excel(
    file_path,
    index=False,
    sheet_name="data",
)

df_to_share_19.to_excel(
    file_path_19,
    index=False,
    sheet_name="data",
)

# Creating the DataFrame
notes_data = {
    "variable": [
        "All Biodiversity variables",
        "All Air Pollution variables",
        "All Nutrient Pollution variables",
    ],
    "notes": [
        "GLOBIO was only connected to IMAGE projections",
        "FASST was only connected to AIM projections",
        "GNM was only connected to IMAGE projections",
    ],
}

vars_dict = {"variable": unique_vars}
df_notes = pd.DataFrame(notes_data)
df_vars = pd.DataFrame(vars_dict)

for file in [file_path, file_path_19]:
    with pd.ExcelWriter(
        file, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        # Write the DataFrame to a new sheet called 'Notes'
        df_notes.to_excel(writer, sheet_name="Notes", index=False)
        df_vars.to_excel(writer, sheet_name="Variables", index=False)
