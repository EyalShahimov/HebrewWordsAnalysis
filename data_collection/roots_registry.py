import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product
from tqdm import tqdm
from .academy_website import AcademyWebsite
from typing import List, Tuple


# Data registry for roots and stems downloaded from the website
class RootsRegistry:
    def __init__(self, file_path: Path, website: AcademyWebsite):
        self.__file_path = file_path
        self.__website = website
        if not self.__file_path.exists():
            self.__download_roots()
        self.dataframe = self.__load_roots()

    def __load_roots(self) -> pd.DataFrame:
        return pd.read_csv(self.__file_path, encoding='utf-16')

    def __download_roots(self) -> None:
        prefixes = self.__generate_size_2_prefixes()
        results = []
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = {executor.submit(self.__fetch_and_parse, prefix): prefix for prefix in prefixes}
            for future in tqdm(as_completed(futures), total=len(prefixes)):
                results.extend(future.result())
        df = pd.DataFrame(results, columns=['root', 'stem'])
        df.to_csv(self.__file_path, index=False, encoding='utf-16')

    def __fetch_and_parse(self, prefix: str) -> List[Tuple[str, str]]:
        return [entry for response in self.__website.fetch_roots(prefix) for entry in response.as_entries()]

    @staticmethod
    def __generate_size_2_prefixes() -> List[str]:
        alephbet = 'אבגדהוזחטיכלמנסעפצקרשת'
        finals = 'ךםןףץ'
        alephbet_with_finals = alephbet + finals
        return [''.join(pair) for pair in product(alephbet, alephbet_with_finals)]