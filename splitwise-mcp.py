from typing import Any
from mcp.server.fastmcp import FastMCP
from splitwise import Splitwise
import os
import requests
import json


mcp = FastMCP()

splitwise_base_url = "https://secure.splitwise.com/api/v3.0"

splitwise_token = os.getenv("SPLITWISE_TOKEN") 
consumer_key = os.getenv("CONSUMER_KEY") 
consumer_secret = os.getenv("CONSUMER_SECRET") 

sobj = Splitwise(consumer_key,consumer_secret,api_key=splitwise_token)

def add_splitwise_expense(cost:int,description:str,group_id:int,split_equally:bool):
    payload = json.dumps({
        "cost": int(cost),
        "description": description,
        "group_id": group_id,
        "split_equally": split_equally
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+splitwise_token
    }
    response = requests.request("POST", splitwise_base_url +"/create_expense", headers=headers, data=payload)
    return response.status_code,response.text

# status,response = add_splitwise_expense(102,"Test - Grocery run",82228382,True)
# print(status,response)


def get_balance(user_id: str) -> str:
    """Get the balance for a user."""
    return "Balance for current user: 100"

@mcp.tool()
async def get_balance(user_id: str) -> str:
    """Get the balance for a user."""
    return "Balance for current user: 100"

@mcp.tool()
async def get_friends(user_id: str) -> str:
    # TODO:  get friends from splitwise
    return ""

@mcp.tool()
async def get_groups() -> str:
    groups = sobj.getGroups()
    group_list = []
    for i in groups:
        gmap = {
            "id": i.id,
            "name": i.name
        }
        group_list.append(gmap)
    return group_list

@mcp.tool()
async def get_expenses(user_id: str) -> str:
    """Get the expenses for a user."""
    return "Expenses for current user: 100"

@mcp.tool()
async def add_expense(cost: float,description: str,group_id: int,split_equally: bool) -> str:
    status,response = add_splitwise_expense(cost,description,group_id,split_equally)
    if status == 200:
        return f"Expense added for current user: {cost} with response: {response}"
    else:
        return "Expense addition failed"





if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
