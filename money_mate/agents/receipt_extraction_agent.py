import logging

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from money_mate.types.receipt_type import Receipt


class ReceiptExtractionAgent:
  PROMPT = """\
You are an expert at extracting information from receipts. Your task is to analyze the receipt image and extract structured information according to the specified format.

Follow these steps carefully:

1. First, scan the entire receipt to identify:
   - Company name/header
   - Date of purchase
   - All individual items and their prices

2. For each item, determine:
   - The exact item name as written
   - The precise price
   - The category, which must be one of: "household", "food", "transportation", "entertainment", "shopping", or "other"

3. Verify that:
   - All prices are correctly formatted as numbers
   - The date follows YYYY-MM-DD format
   - Each item is categorized into one of the allowed categories

Here are examples of good analyses:

<example>
<input>
Receipt from Walmart
2024-01-15
Banana $1.99
Light bulbs $5.99
Movie ticket $12.99
Toothpaste $3.99
Gas $45.00
T-shirt $15.99
</input>
<thinking>
1. Company identification: Clear header shows "Walmart"
2. Date: Already in correct format 2024-01-15
3. Items analysis:
   - "Banana" -> food category, price $1.99
   - "Light bulbs" -> household category, price $5.99
   - "Movie ticket" -> entertainment category, price $12.99
   - "Toothpaste" -> household category, price $3.99
   - "Gas" -> transportation category, price $45.00
   - "T-shirt" -> shopping category, price $15.99
4. Verification: All prices are numerical, date is correct format, categories match allowed list
</thinking>
<output>
{
  "company": "Walmart",
  "date": "2024-01-15",
  "items": [
    {"name": "Banana", "price": 1.99, "type": "food"},
    {"name": "Light bulbs", "price": 5.99, "type": "household"},
    {"name": "Movie ticket", "price": 12.99, "type": "entertainment"},
    {"name": "Toothpaste", "price": 3.99, "type": "household"},
    {"name": "Gas", "price": 45.00, "type": "transportation"},
    {"name": "T-shirt", "price": 15.99, "type": "shopping"}
  ]
}
</output>
</example>

Now, please analyze the provided receipt image following these steps and provide the information in the required format. Remember to only use these categories: "household", "food", "transportation", "entertainment", "shopping", or "other". If you're unsure about a category, use "other".

Let me think through this carefully:

1. First, I'll examine the overall receipt structure...
2. Then, I'll identify and list each item...
3. Finally, I'll categorize everything into the allowed categories and format the output...
"""

  def __init__(self, model_name: str, api_key: str):
    model = ChatOpenAI(model=model_name, api_key=api_key)
    self.structured_llm = model.with_structured_output(Receipt)
    self.logger = logging.getLogger("money_mate.agents.receipt_extraction_agent")

  def scan_image_bytes(self, image_base64: bytes) -> Receipt:
    self.logger.info("Processing a new image bytes")
    message = HumanMessage(
      content=[
        {"type": "text", "text": self.PROMPT},
        {
          "type": "image_url",
          "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
        },
      ],
    )
    return self.structured_llm.invoke([message])
