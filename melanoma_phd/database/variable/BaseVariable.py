from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Union

import pandas as pd

from melanoma_phd.database.variable.BaseVariableConfig import BaseVariableConfig

PValue = float


class VariableType(Enum):
    SCALAR = "scalar"
    CATEGORICAL = "categorical"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    ITERATED = "iterated"


@dataclass
class BaseVariable(ABC):
    def __init__(self, config: BaseVariableConfig) -> None:
        self.id: str = config.id
        self.name: str = config.name
        self.selectable: bool = config.selectable
        self.unique_id: Optional[str] = None

    def __hash__(self) -> int:
        return hash(self.id)

    @abstractmethod
    def init_from_dataframe(self, dataframe: pd.DataFrame) -> None:
        self._check_valid_id(dataframe)
        self.unique_id = (
            f"{dataframe.name}.{self.id}" if hasattr(dataframe, "name") else f"{self.id}"
        )

    @abstractmethod
    def get_series(self, dataframe: pd.DataFrame) -> pd.Series:
        return dataframe[self.id]

    @abstractmethod
    def descriptive_statistics(
        self,
        dataframe: pd.DataFrame,
        group_by: Optional[Union[BaseVariable, List[BaseVariable]]] = None,
        **kwargs: Any,
    ) -> pd.DataFrame:
        pass

    @abstractmethod
    def format_descriptive_statistics(
        self,
        dataframe: pd.DataFrame,
    ) -> List[List[str]]:
        pass

    @abstractmethod
    def _check_valid_id(self, dataframe: pd.DataFrame) -> None:
        if self.id not in dataframe.columns:
            raise ValueError(f"'{self.id}' not present in dataframe")

    def _get_non_na_data(self, data: Union[pd.DataFrame, pd.Series]) -> pd.Series:
        if isinstance(data, pd.DataFrame):
            return self.get_series(dataframe=data).dropna()
        else:
            return data
