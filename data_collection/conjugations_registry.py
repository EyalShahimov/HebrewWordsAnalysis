import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from .academy_website import AcademyWebsite


# Data registry for conjugations downloaded from the website
class ConjugationsRegistry:
    def __init__(self, file_path: Path, website: AcademyWebsite, roots_df: pd.DataFrame):
        self.__file_path = file_path
        self.__website = website
        self.__roots_df = roots_df
        if not self.__file_path.exists():
            self.__download_conjugations()
        self.dataframe = self.__load_conjugations()

    def __load_conjugations(self) -> pd.DataFrame:
        return pd.read_csv(self.__file_path, encoding='utf-16')

    def __download_conjugations(self) -> None:
        results = []
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = {executor.submit(self.__fetch_and_parse, e): e for e in self.__roots_df.iterrows()}
            for future in tqdm(as_completed(futures), total=len(futures)):
                df = future.result()
                if not df.empty:
                    results.extend(df.values.tolist())
        df = pd.DataFrame(results, columns=['root', 'stem', 'tense', 'pronoun', 'conjugation']).drop_duplicates()
        df.to_csv(self.__file_path, index=False, encoding='utf-16')

    def __fetch_and_parse(self, e):
        _, (root, stem) = e
        responses = self.__website.fetch_conjugations(root, stem)
        rows = [entry for response in responses for entry in response.get_entries()]
        return pd.DataFrame(rows) if rows else pd.DataFrame()