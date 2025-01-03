import json
import logging
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd
import streamlit as st

from money_mate.types.receipt_type import Receipt


class ReceiptHandler:
  RECEIPT_JSON_FILENAME = "scanned_receipts.json"
  ENCODING = "utf-8"

  def __init__(self):
    self.logger = logging.getLogger("money_mate.handler.receipt_handler")

    self.receipt_file = Path(st.secrets["working_dir"]) / self.RECEIPT_JSON_FILENAME
    self.receipt_file.parent.mkdir(parents=True, exist_ok=True)

    self.receipts = []
    self._load_existing_receipts()

  def _load_existing_receipts(self):
    if self.receipt_file.exists():
      self.logger.info(f"Loading existing receipt from {self.receipt_file}")
      with self.receipt_file.open(encoding=self.ENCODING) as f:
        for line in f:
          self.receipts.append(Receipt.model_validate_json(json.loads(line)))
      self.logger.info(f"Loaded {len(self.receipts)} receipts from {self.receipt_file}")

  def save_new_receipt(self, receipt: Receipt):
    self.receipts.append(receipt)
    with self.receipt_file.open("a", encoding=self.ENCODING) as f:
      json.dump(receipt.model_dump_json(), f)
      f.write("\n")
    self.logger.info(f"Saved new receipt, now we have {len(self.receipts)} receipts.")

  def filter_receipts_by_date(
    self, start_date: Optional[date] = None, end_date: Optional[date] = None
  ) -> Sequence[Receipt]:
    filtered_receipt = self.receipts
    if start_date:
      filtered_receipt = [
        receipt
        for receipt in filtered_receipt
        if start_date <= datetime.strptime(receipt.date, "%Y-%m-%d").date()
      ]

    if end_date:
      filtered_receipt = [
        receipt
        for receipt in filtered_receipt
        if datetime.strptime(receipt.date, "%Y-%m-%d").date() <= end_date
      ]

    return filtered_receipt

  def aggregate_spending_by_category(
    self, start_date: Optional[date] = None, end_date: Optional[date] = None
  ):
    filtered_receipt = self.filter_receipts_by_date(start_date, end_date)
    category_totals = defaultdict(float)
    for receipt in filtered_receipt:
      for item in receipt.items:
        category = item.category
        price = item.price
        category_totals[category] += price
    return category_totals

  def aggregate_spending_by_company(self, start_date: date, end_date: date):
    """Aggregate spending by company."""
    filtered_receipt = self.filter_receipts_by_date(start_date, end_date)
    company_totals = defaultdict(float)
    for receipt in filtered_receipt:
      for item in receipt.items:
        price = item.price
        company = receipt.company
        company_totals[company] += price
    return company_totals

  def aggregate_spending_by_date(self, start_date: date, end_date: date):
    """Aggregate total spending by date."""
    filtered_receipt = self.filter_receipts_by_date(start_date, end_date)
    date_totals = defaultdict(float)
    for receipt in filtered_receipt:
      date = receipt.date
      for item in receipt.items:
        price = item.price
        date_totals[date] += price
    return date_totals

  def to_pandas_dataframe(self) -> pd.DataFrame:
    table_data = []
    for receipt in self.receipts:
      for item in receipt.items:
        table_data.append(
          {
            "Company": receipt.company,
            "Date": receipt.date,
            "Item Name": item.name,
            "Price": item.price,
            "Category": item.category,
          }
        )
    return pd.DataFrame(table_data)

  def to_string(self):
    receipts_str = ""
    for index, receipt in enumerate(self.receipts):
      receipts_str += f"Receipt number {index+1}\n\n"
      receipts_str += str(receipt) + "\n\n"
    return receipts_str
