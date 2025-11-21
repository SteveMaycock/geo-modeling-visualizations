import pandas as pd
import pyam
from pathlib import Path

df_slice_mapping = pd.read_excel(
    "./././data/TOD/model_results/raw/variable_list_for_chapters.xlsx",
    sheet_name="Variables",
)

df_all_chapters = pyam.IamDataFrame(
    "./././data/TOD/model_results/to_share/model_results_to_share.xlsx"
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
    file_path = f"./././data/TOD/model_results/to_share/model_results_to_share_{chapter_name}.xlsx"

    # Ensure output directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

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

    # Write all sheets in one go to avoid corruption
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        df_to_share.to_excel(writer, sheet_name="data", index=False)
        df_notes.to_excel(writer, sheet_name="Notes", index=False)
        df_vars.to_excel(writer, sheet_name="Variables", index=False)

