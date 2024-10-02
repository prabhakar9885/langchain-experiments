from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Any


class PersonDetails(BaseModel):
    name: str = Field(description="Full name")
    summary: str = Field(description="Summary")
    facts: List[str] = Field(description="Interesting facts")
    profiles: List[str] = Field(description="List of URLs for the online profiles")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "summary": self.summary,
            "facts": self.facts,
            "onlineProfiles": self.profiles
        }


person_output_parser = PydanticOutputParser(pydantic_object=PersonDetails)
