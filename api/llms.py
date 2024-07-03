import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from typing import Any

import langchain
from langchain.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.prompts import PromptTemplate
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.messages import HumanMessage

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.schema import HumanMessage, SystemMessage
from langchain.agents import Tool, tool
from langchain.chains import LLMChain




model_for_order_id = ChatOllama(
    model="phi3",
    keep_alive=-1,
    format="json",
    temperature = 0.0,
    cache = False,
    top_k = 5
    )

function_calling_model = OllamaFunctions(
    model="phi3",
    keep_alive=-1,
    format="json",
    temperature = 0.0,
    cache = False,
    top_k = 5
    )


model_for_function_calling = function_calling_model.bind_tools(
    tools=[
        {
            "name": "GetOrderDetails",
            "description": "This should be called when user wants to know details of the product, details will contain order date, delivery date, product name, price etc",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
         {
            "name": "CancelOrder",
            "description": "This function should be called when user requests for order cancellation",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "GetOrderStatus",
            "description": "This function should be called to get order status like, when the order would be delivered? or when I would receive it? or why my is my order delayed? or my havent I rceived my order etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "GetRefundStatus",
            "description": "Get refund status, This function is to know refund status of order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "ReturnOrder",
            "description": "This function should be called when user wants to cancel an order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "ReplaceOrder",
            "description": "Replace an order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "NotReceived",
            "description": "Call this function if user complaints that order not received or not delivered yet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "DownloadInvoice",
            "description": "Call this function if user wants invoice for the order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "CashbackOrRewards",
            "description": "Call this function if user wants to know about cash back or rewards",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "ReturnPolicy",
            "description": "Call this function if user wants to know return policy",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "CancellationPolicy",
            "description": "Call this function if user wants to know cancellation policy",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "ReplacementPolicy",
            "description": "Call this function if user wants to know Replacement policy",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "OrderTracking",
            "description": "Call this function if user wants to track the order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "ChangeDelivaryTime",
            "description": "Call this function if user wants to change delivery date, if user requests for sooner or delayed delivery",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "HumanSupport",
            "description": "Call this function if user wants human support",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "order id in string like ord12345",
                    },
                }
            },
        },
        {
            "name": "__conversational_response",
            "description": (
                "Respond conversationally if no other tools should be called for a given query."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "response": {
                        "type": "string",
                        "description": "Conversational response to the user.",
                    },
                },
                "required": ["response"],
            },
        },

    ],
    functions_to_call=["__conversational_response", "GetOrderDetails", "CancelOrder", "GetOrderStatus", "GetRefundStatus", "ReturnOrder", "ReplaceOrder"]
)


prompt_template_for_function_calling = """
You are a seasoned customer support executive at a e commerece company. You can greet the user and explain how you can help. Always obey system messages.
You should choose right tool based on users query
You have access to following tools, you should always choose atleast one of them.

__conversational_response(response: str) -> str - Respond conversationally if no other tools should be called for a given query or you dont have enough data to use any other functions
GetOrderDetails() -> str - Get order details.
CancelOrder() -> str - call this function to cancel an order.
GetOrderStatus() -> str - Get order status, This function is to know delivary status of order.
GetRefundStatus() -> str - Get refund status, This function is to know refund status of order.
ReturnOrder() -> str - Return an order.
ReplaceOrder() -> str - Replace an order.
HumanSupport() -> str - Call this function if user wants human support
ChangeDelivaryTime() -> str - Call this function if user wants to change delivery date, if user requests for sooner or delayed delivery
OrderTracking() -> str - Call this function if user wants to track the order
ReplacementPolicy() -> str - Call this function if user wants to know Replacement policy
CancellationPolicy() -> str - Call this function if user wants to know cancellation policy
ReturnPolicy() -> str - Call this function if user wants to know return policy.
CashbackOrRewards() -> str - Call this function if user wants to know about cash back or rewards
DownloadInvoice() -> str - Call this function if user wants invoice for the order
NotReceived() -> str - Call this function if user complaints that order not received or not delivered yet.

Use the following format:

Question: the customer query you must support
Thought: Think what is the appropriate action to take.
tool: the action to take, should be one of [__conversational_response, GetOrderDetails, CancelOrder, GetOrderStatus, GetRefundStatus, ReturnOrder, ReplaceOrder], you should always return atleast one of these tools
tool_input: the input to the action, note for __conversational_response the input should be your response

Begin!
"""

prompt_template = f"""
You are a seasoned customer support executive at a quick commerece company. You can greet the user and explain the user that you can help with selecting users past purchases and ask user to start explaining the purchase or product. Always obey system messages.
If the user asks for details, cancel any order or any other request with order, you should always explain user that you would need an order id to excecute any function/tool.

Below is the purchase history of user, based on it you need to return correct order ids

purchase_history:
products_go_here

Begin!
"""