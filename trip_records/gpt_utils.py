import os
from typing import Type, List

from langchain_core.output_parsers import PydanticOutputParser
from openai import OpenAI
from pydantic import BaseModel, Field

from trip_records.models import DriverTripRecord


class Journey(BaseModel):
    customer_name: str = Field(description="Name of the customer")
    city: str = Field(description="City of the customer")
    state: str = Field(description="State of the customer")
    pallets_in: int = Field(description="Number of pallets in")
    pallets_out: int = Field(description="Number of pallets out")
    time_in: str = Field(description="Time in HH:MM")
    time_out: str = Field(description="Time out HH:MM")
    mileage: str = Field(description="calculate mileage between two locations")
    start_route: str = Field(description="Start route initial route or the previous route")
    end_route: str = Field(description="End route the route as per the city and state and if last visit then ending location")
    comments: str = Field(description="Comments of the route")


class TripsData(BaseModel):
    journey: List[Journey] = Field(description="Generate journey list for every route submitted to you")


class OpenAICompletionClient:
    def __init__(self, model_name: str):
        api_key = os.getenv("OPENAI_API_KEY")  # Load API key from environment variables
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def send_request(self, data, start_location, ending_location):
        temperature = 0.3
        parser = PydanticOutputParser(pydantic_object=TripsData)
        prompt_template = f'''
            You are our travel logger and report preparer. We submit this data, which is route information from the start of a journey at {start_location} to one place and then to other locations.
            You will output in JSON a list of journey routes, calculating estimated mileage based on location city and ZIP code provided, and also mention the start and end routes.
            Other information is produced as it is. You will also calculate the estimated time in and time out for that location, adding 30 minutes to the start and end time to make travel realistic.
            The data is {data}, and the ending location is {ending_location}.
            *Format instructions:
            {parser.get_format_instructions()}
            End instructions.
            Reply only in JSON format as per the instructions.
        '''

        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=temperature,
            top_p=0.5,
            frequency_penalty=0.2,
            presence_penalty=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Remember to strictly follow JSON format provided in instructions."},
                {"role": "user", "content": prompt_template}
            ]
        )
        cost_of_call = self.calculate_cost(response.usage.completion_tokens, response.usage.prompt_tokens)
        print(f"Cost of this call: ${cost_of_call:.4f}")

        raw_response = response.choices[0].message.content
        parsed_response = parser.parse(raw_response)
        return parsed_response.dict()

    @staticmethod
    def calculate_cost(completion_tokens: int, prompt_tokens: int) -> float:
        completion_price_per_token = 0.03 / 1000
        prompt_price_per_token = 0.01 / 1000
        return (completion_price_per_token * completion_tokens) + (prompt_price_per_token * prompt_tokens)