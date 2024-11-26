from pydantic import BaseModel, Field
from typing import List
from dataclasses import dataclass
from langchain_openai import OpenAI, ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.callbacks import get_openai_callback
import os

class ReceiptItem(BaseModel):
    """Information about a single item on a reciept"""

    item_name: str = Field("The name of the purchased item")
    item_cost: str = Field("The cost of the item")
    item_type: str = Field("The type of the item")


class ReceiptInformation(BaseModel):
    """Information extracted from a receipt"""

    vendor_name: str = Field(
        description="The name of the company who issued the reciept"
    )
    datetime: str = Field(
        description="The date and time that the receipt was printed in MM/DD/YY HH:MM format"
    )
    items_purchased: List[ReceiptItem] = Field(description="List of purchased items")
    tax_rate: str = Field(description="The tax rate applied")
    total: str = Field(description="The total cost after tax")
    
class ReceiptAnalyzer:

    def __init__(self, openai_api_key: str, chat_model: str = "gpt-4o-mini"):
        self.openai_api_key = openai_api_key
        self.llm = ChatOpenAI(model=chat_model, api_key=openai_api_key)
        self.setup_chain()

    def setup_chain(self):
    #Set up the LangChain prompt template and chain
        template = """
        Analyze this receipt text and extract the following information in a structured format:
        
        Receipt Text:
        {receipt_text}
        
        Please extract and format the following information:
        1. Vendor Name
        2. Date and Time (in MM/DD/YY HH:MM format)
        3. List of items purchased (with name, cost, and type)
        4. Tax rate
        5. Total amount after tax

        If any information is missing, use "N/A".
        
        Format your response as a JSON object matching this structure:
        {
            "vendor_name": "",
            "datetime": "",
            "items_purchased": [
                {
                    "item_name": "",
                    "item_cost": "",
                    "item_type": ""
                }
            ],
            "tax_rate": "",
            "total": ""
        }
        """
    
        self.prompt = PromptTemplate(
            input_variables=["receipt_text"],
            template=template
        )
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt
        )

    def analyze_receipt(self, receipt_text: str) -> dict:
        """
        Analyze the receipt text and return structured information
        
        Args:
            receipt_text (str): The extracted text from the receipt image
            
        Returns:
            dict: Structured receipt information
        """
        try:
            with get_openai_callback() as cb:
                result = self.chain.run(receipt_text=receipt_text)
                print(f"Tokens used: {cb.total_tokens}")
                print(f"Cost: ${cb.total_cost}")
            
            return result
        except Exception as e:
            return {
                "error": f"Failed to analyze receipt: {str(e)}",
                "raw_text": receipt_text
            }
        
def create_analyzer(api_key: str = None) -> ReceiptAnalyzer:
    """
    Create a ReceiptAnalyzer instance with the provided or environment API key
    """
    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key is None:
            raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")
    
    return ReceiptAnalyzer(api_key)
