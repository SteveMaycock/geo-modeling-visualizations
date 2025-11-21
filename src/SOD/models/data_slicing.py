import pandas as pd
import pyam

df_slice_mapping = pd.read_excel(
    "./././data/SOD/model_results/raw/variable_list_for_chapters.xlsx",
    sheet_name="Variables",
)

df_all_chapters = pyam.IamDataFrame(
    "./././data/SOD/model_results/to_share/model_results_to_share.xlsx"
)
# Chapter 19 done later in file
for chapter in [
    "Chapter 14 - Economics",
    "Chapter 15 - Circularity",
    "Chapter 16 - Energy",
    "Chapter 17 - Food",
    "Chapter 18 - Environment",
    "Outlooks",
    "Chapter 20",
    "Chapter 21",
]:

    df_slice_mapping_chapter = df_slice_mapping.dropna(subset=[chapter])
    chapter_vars = df_slice_mapping_chapter.variable.unique()

    df_chapter = df_all_chapters.filter(variable=chapter_vars)

    df_to_share = df_chapter.timeseries().reset_index()
    df_to_share = df_to_share.rename(columns={"model": "topic"})
    chapter_name = chapter.replace(" - ", "_").replace(" ", "_")
    file_path = f"./././data/SOD/model_results/to_share/model_results_to_share_{chapter_name}.xlsx"
    df_to_share.to_excel(
        file_path,
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

    vars_dict = {"variable": df_chapter.variable}

    df_notes = pd.DataFrame(notes_data)
    df_vars = pd.DataFrame(vars_dict)

    with pd.ExcelWriter(
        file_path, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        # Write the DataFrame to a new sheet called 'Notes'
        df_notes.to_excel(writer, sheet_name="Notes", index=False)
        df_vars.to_excel(writer, sheet_name="Variables", index=False)
