import logging
import dataclasses
from typing import Any

import pandas as pd

from mymoney.institutions import amex
from mymoney.institutions import capitalone
from mymoney.institutions import chase
from mymoney.institutions import citi
from mymoney.institutions import discover
from mymoney.institutions import paypal
from mymoney.institutions import venmo


logging.basicConfig(
    level=logging.INFO,
    format="%(name)s\t[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%b/%d/%y %I:%M:%S %p",
    # filename="logs.log",
)


@dataclasses.dataclass
class InstData:
    """Main class for storing and transforming Institution data."""
    # input data
    source: str | Any
    data_type: Any
    institution_name: str
    service_name: str
    account_name: str
    table: pd.DataFrame | Any

    # output data
    sanity_df: pd.DataFrame = None
    output_df: pd.DataFrame = None
    out_type: str = None

    def __init__(
        self,
        source: str | Any,
        data_type: Any,
        institution_name: str,
        service_name: str,
        account_name: str,
        table: pd.DataFrame | Any,
    ) -> None:
        self.source = source
        self.data_type = data_type
        self.institution_name = institution_name
        self.service_name = service_name
        self.account_name = account_name
        self.table = table

        self.create_output_data()

    def _generate_file_name(self) -> str:
        """Generate a unique file name in the following format:
        ``<INSTITUTION NAME> - <SERVICE NAME> -
            <ACCOUNT NAME> (<LAST DATE APPEARED IN THE DATA>)``."""
        last_date = str(self.output_df["Date"].max().date())
        return (
            f"{self.institution_name} - {self.service_name} -"
            f" {self.account_name} ({last_date})"
        )

    def _institution_executer(self) -> pd.DataFrame:
        """Returns the `sanity_df` DataFrame. Basically this method creates
        an object corresponding to the `institution_name` and
        call `service_executer` method to do the operations."""
        match self.institution_name:
            case "amex": inst_obj = amex.AmEx()
            case "capitalone": inst_obj = capitalone.CapitalOne()
            case "chase": inst_obj = chase.Chase()
            case "citi": inst_obj = citi.Citi()
            case "discover": inst_obj = discover.Discover()
            case "paypal": inst_obj = paypal.PayPal()
            case "venmo": inst_obj = venmo.Venmo()
            case _:
                raise ValueError(
                    f"Institution {self.institution_name} is not supported."
                    "\nYou can file an issue and provide more information"
                    " to add the institution."
                )

        return inst_obj.service_executer(
            service_name=self.service_name, data_type=self.data_type,
            table=self.table, account_name=self.account_name
        )

    def _output_df_creator(self, sanity_df: pd.DataFrame) -> pd.DataFrame:
        """Creates a DataFrame aligned with `output_df` schema from `sanity_df`

        Args:
            sanity_df (pd.DataFrame):
                The input DataFrame.

        Returns:
            A DataFrame with the `output_df` schema.
        """
        new_columns_name_map = {
            col: col[5:]
            for col in sanity_df.columns
            if col.startswith("_new_")
        }
        old_columns = [
            col
            for col in sanity_df.columns
            if not col.startswith("_new_")
        ]

        return sanity_df.drop(columns=old_columns).rename(
            columns=new_columns_name_map
        )

    def _set_out_type(self):
        """Set the `out_type` based on `service_name`."""
        match self.service_name:
            case "debit": out_type = "balance"
            case "credit": out_type = "expense"
            case "3rdparty": out_type = "expense"
            case "exchange": out_type = "trade"
            case _:
                raise ValueError(
                    "service_name should be one of the following:"
                    " ['debit', 'credit', '3rdparty', 'exchange']."
                )

        self.out_type = out_type

    def create_output_data(self):
        """Create the output data."""
        self.sanity_df = self._institution_executer()
        self.output_df = self._output_df_creator(self.sanity_df)
        self._set_out_type()


@dataclasses.dataclass
class MyData:
    """Main class for storing MyMoney core data and analysis."""
    expense: pd.DataFrame
    trade: pd.DataFrame
    balance: pd.DataFrame
